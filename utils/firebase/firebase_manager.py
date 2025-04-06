import threading
import firebase_admin
from firebase_admin import credentials
from utils.config import config, env
from utils.firebase.firebase_reference import ReferenceWrapper
from utils.tracing.firebase_decorators import log_firebase_operation
from utils.tracing.logger_utils import get_logger

class FirebaseManager:
    _instances = {}
    _lock = threading.Lock()

    def __init__(self, app_name: str, credentials_path: str, database_url: str):
        self.app_name = app_name
        self.credentials_path = credentials_path
        self.database_url = database_url
        self.app = None

        logger_name = f"firebase.{app_name}"
        config_logger_level = config[env].FIREBASE_MGR_LOGGER_LOG_LEVEL
        config_logger_mode = config[env].FIREBASE_MGR_LOGGER_LOG_CHANNELS

        self.logger = get_logger(name=logger_name, level=config_logger_level, mode=config_logger_mode)

    @classmethod
    def get_instance(cls, app_name, credentials_path=None, database_url=None):
        with cls._lock:
            if app_name in cls._instances:
                return cls._instances[app_name]

            if not credentials_path or not database_url:
                raise ValueError(f"Credenziali e database_url obbligatori per '{app_name}'")

            instance = cls(app_name, credentials_path, database_url)
            instance.initialize()
            cls._instances[app_name] = instance
            return instance

    def initialize(self):
        protected_app_name = self.app_name if self.app_name is not None else "MISSING-FIREBASE-DATABASE-APP-NAME"
        protected_database_url = self.database_url if self.database_url is not None else "MISSING-FIREBASE-DATABASE-URL"
        protected_credentials_path = self.credentials_path if self.credentials_path is not None else "MISSING-FIREBASE-DATABASE-CREDENTIALS-PATH"

        if self.app:
            self.logger.info("Firebase app già inizializzata.")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [database_url]: [{protected_database_url}]")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [credentials_path]: [{protected_credentials_path}]")
            return
        try:
            cred = credentials.Certificate(self.credentials_path)
            self.app = firebase_admin.initialize_app(cred, {
                'databaseURL': self.database_url
            }, name=self.app_name)
            self.logger.info("Firebase app inizializzata correttamente.")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [database_url]: [{protected_database_url}]")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [credentials_path]: [{protected_credentials_path}]")
        except Exception as e:
            self.logger.error(f"Errore durante l'inizializzazione: {e}")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [database_url]: [{protected_database_url}]")
            self.logger.debug(f"Firebase app [{protected_app_name}], PARAM [credentials_path]: [{protected_credentials_path}]")
            raise

    @log_firebase_operation
    def get_reference(self, path="/"):
        if not self.app:
            raise RuntimeError(f"App '{self.app_name}' non inizializzata.")
        return ReferenceWrapper(path, self.app)
