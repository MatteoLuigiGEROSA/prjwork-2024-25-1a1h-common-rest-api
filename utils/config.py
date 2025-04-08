import os

env = os.getenv("FLASK_ENV", "development")


class Config:
    FLASK_WEBAPP_NAME = os.getenv("FLASK_WEBAPP_NAME", "flask-webapp")
    DEBUG = False

    LOGS_DIR =                         os.getenv("LOGS_DIR", "logs")
    LOG_LEVEL_ALL_MODULES_DEFAULT =    os.getenv("LOG_LEVEL_ALL_MODULES_DEFAULT", "ERROR")
    LOG_CHANNELS_ALL_MODULES_DEFAULT = os.getenv("LOG_CHANNELS_ALL_MODULES_DEFAULT", "f") # "c"->console, "f"->file, "cf"->console+file

    APP_CONTROLLER_LOGGER_LOG_LEVEL =    os.getenv("APP_CONTROLLER_LOGGER_LOG_LEVEL", "INFO")
    APP_CONTROLLER_LOGGER_LOG_CHANNELS = os.getenv("APP_CONTROLLER_LOGGER_LOG_CHANNELS", "cf") # "c"->console, "f"->file, "cf"->console+file

    MIN_VELOCITA_TRENI_AT_PAL = os.getenv("MIN_VELOCITA_TRENI_AT_PAL",  "10")
    MAX_VELOCITA_TRENI_AT_PAL = os.getenv("MAX_VELOCITA_TRENI_AT_PAL", "140")

    MIN_ATTESA_TRENI_AT_PAL_MIN     = os.getenv("MIN_ATTESA_TRENI_AT_PAL_SEC",       "5")
    MAX_ATTESA_TRENI_AT_PAL_MIN     = os.getenv("MAX_ATTESA_TRENI_AT_PAL_SEC",      "15")
    DEFAULT_ATTESA_TRENI_AT_PAL_MIN = os.getenv("DEFAULT_ATTESA_TRENI_AT_PAL_MIN", "120")

    PASSAGGIO_VOID_VALUE_LABEL  = os.getenv("PASSAGGIO_VOID_VALUE_LABEL",  "valore-stato-transito-non-codificato")
    PASSAGGIO_APERTO_TAG        = os.getenv("PASSAGGIO_APERTO_TAG",        "0")
    PASSAGGIO_APERTO_LABEL      = os.getenv("PASSAGGIO_APERTO_LABEL",      "passaggio-aperto-agibile")
    PASSAGGIO_CHIUSO_TAG        = os.getenv("PASSAGGIO_CHIUSO_TAG",        "1")
    PASSAGGIO_CHIUSO_LABEL      = os.getenv("PASSAGGIO_CHIUSO_LABEL",      "passaggio-chiuso-interrotto")
    PASSAGGIO_IN_APERTURA_TAG   = os.getenv("PASSAGGIO_IN_APERTURA_TAG",   "2")
    PASSAGGIO_IN_APERTURA_LABEL = os.getenv("PASSAGGIO_IN_APERTURA_LABEL", "passaggio-in-riapertura")
    PASSAGGIO_IN_CHIUSURA_TAG   = os.getenv("PASSAGGIO_IN_CHIUSURA_TAG",   "3")
    PASSAGGIO_IN_CHIUSURA_LABEL = os.getenv("PASSAGGIO_IN_CHIUSURA_LABEL", "passaggio-in-chiusura")


class DevelopmentConfig(Config):
    DEBUG = True

    RESTFUL_API_LOGGER_LOG_LEVEL =     os.getenv("RESTFUL_API_LOGGER_LOG_LEVEL", "DEBUG")
    RESTFUL_API_LOGGER_LOG_CHANNELS =  os.getenv("RESTFUL_API_LOGGER_LOG_CHANNELS_", "f") # "c"->console, "f"->file, "cf"->console+file
    VIEW_MODEL_LOGGER_LOG_LEVEL =      os.getenv("VIEW_MODEL_LOGGER_LOG_LEVEL", "DEBUG")
    VIEW_MODEL_LOGGER_LOG_CHANNELS =   os.getenv("VIEW_MODEL_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file
    FIREBASE_MGR_LOGGER_LOG_LEVEL =    os.getenv("FIREBASE_MGR_LOGGER_LOG_LEVEL", "INFO")
    FIREBASE_MGR_LOGGER_LOG_CHANNELS = os.getenv("FIREBASE_MGR_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file
    FIREBASE_OPS_LOGGER_LOG_LEVEL =    os.getenv("FIREBASE_OPS_LOGGER_LOG_LEVEL", "INFO")
    FIREBASE_OPS_LOGGER_LOG_CHANNELS = os.getenv("FIREBASE_OPS_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file

    # JSON endpoint(s) & credentials-file based configuration:
    MAIN_DATABASE_1A_URL =         os.getenv("MAIN_DATABASE_1A_URL", "https://allenamento1a2025-default-rtdb.firebaseio.com")
    MAIN_DATABASE_1A_CREDENTIALS = os.getenv("MAIN_DATABASE_1A_CREDENTIALS", "creds/allenamento1a2025-firebase-adminsdk-fbsvc-866d687579.json")
    MAIN_DATABASE_1H_URL =         os.getenv("MAIN_DATABASE_1H_URL", "https://passaggiolivello-2ffe6-default-rtdb.firebaseio.com")
    MAIN_DATABASE_1H_CREDENTIALS = os.getenv("MAIN_DATABASE_1H_CREDENTIALS", "creds/passaggiolivello-2ffe6-firebase-adminsdk-fbsvc-93607d7cea.json")

    # Direct 1A set-env credentials configuration (web-pages testing purposes *only*):
    MAIN_DATABASE_1A_API_KEY =             os.getenv("MAIN_DATABASE_1A_API_KEY", "")
    MAIN_DATABASE_1A_AUTH_DOMAIN =         os.getenv("MAIN_DATABASE_1A_AUTH_DOMAIN", "piattaformariflessi.firebaseapp.com")
    MAIN_DATABASE_1A_PROJECT_ID =          os.getenv("MAIN_DATABASE_1A_PROJECT_ID", "piattaformariflessi")
    MAIN_DATABASE_1A_STORAGE_BUCKET =      os.getenv("MAIN_DATABASE_1A_STORAGE_BUCKET", "piattaformariflessi.firebasestorage.app")
    MAIN_DATABASE_1A_MESSAGING_SENDER_ID = os.getenv("MAIN_DATABASE_1A_MESSAGING_SENDER_ID", "")
    MAIN_DATABASE_1A_APP_ID =              os.getenv("MAIN_DATABASE_1A_APP_ID", "")
    # Direct 1H set-env credentials configuration (web-pages testing purposes *only*):
    MAIN_DATABASE_1H_API_KEY =             os.getenv("MAIN_DATABASE_1H_API_KEY", "")
    MAIN_DATABASE_1H_AUTH_DOMAIN =         os.getenv("MAIN_DATABASE_1H_AUTH_DOMAIN", "passaggioalivello.firebaseapp.com")
    MAIN_DATABASE_1H_PROJECT_ID =          os.getenv("MAIN_DATABASE_1H_PROJECT_ID", "passaggioalivello")
    MAIN_DATABASE_1H_STORAGE_BUCKET =      os.getenv("MAIN_DATABASE_1H_STORAGE_BUCKET", "passaggioalivello.firebasestorage.app")
    MAIN_DATABASE_1H_MESSAGING_SENDER_ID = os.getenv("MAIN_DATABASE_1H_MESSAGING_SENDER_ID", "")
    MAIN_DATABASE_1H_APP_ID =              os.getenv("MAIN_DATABASE_1H_APP_ID", "")


class ProductionConfig(Config):
    DEBUG = False
    # LOG_LEVEL = "ERROR"
    # LOG_CHANNELS = os.getenv("LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file

    # JSON endpoint(s) & credentials-file based configuration:
    RESTFUL_API_LOGGER_LOG_LEVEL =     os.getenv("RESTFUL_API_LOGGER_LOG_LEVEL", "ERROR")
    RESTFUL_API_LOGGER_LOG_CHANNELS =  os.getenv("RESTFUL_API_LOGGER_LOG_CHANNELS_", "f") # "c"->console, "f"->file, "cf"->console+file
    VIEW_MODEL_LOGGER_LOG_LEVEL =      os.getenv("VIEW_MODEL_LOGGER_LOG_LEVEL", "ERROR")
    VIEW_MODEL_LOGGER_LOG_CHANNELS =   os.getenv("VIEW_MODEL_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file
    FIREBASE_MGR_LOGGER_LOG_LEVEL =    os.getenv("FIREBASE_MGR_LOGGER_LOG_LEVEL", "ERROR")
    FIREBASE_MGR_LOGGER_LOG_CHANNELS = os.getenv("FIREBASE_MGR_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file
    FIREBASE_OPS_LOGGER_LOG_LEVEL =    os.getenv("FIREBASE_OPS_LOGGER_LOG_LEVEL", "ERROR")
    FIREBASE_OPS_LOGGER_LOG_CHANNELS = os.getenv("FIREBASE_OPS_LOGGER_LOG_CHANNELS", "f") # "c"->console, "f"->file, "cf"->console+file


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig

}
