from utils.firebase.firebase_manager import FirebaseManager

class FirebaseInitializer:
    def __init__(self, config: dict):
        self._instances = {}
        self._config = config

    def initialize_all(self):
        """
        Inizializza tutte le app Firebase definite nella configurazione.
        """
        self._instances['db_app_1a'] = FirebaseManager.get_instance(
            app_name='db_app_1a',
            credentials_path=self._config.MAIN_DATABASE_1A_CREDENTIALS,
            database_url=self._config.MAIN_DATABASE_1A_URL
        )

        self._instances['db_app_1h'] = FirebaseManager.get_instance(
            app_name='db_app_1h',
            credentials_path=self._config.MAIN_DATABASE_1H_CREDENTIALS,
            database_url=self._config.MAIN_DATABASE_1H_URL
        )

    def get(self, app_name: str) -> FirebaseManager:
        if app_name not in self._instances:
            raise ValueError(f"Firebase app '{app_name}' non inizializzata")
        return self._instances[app_name]
