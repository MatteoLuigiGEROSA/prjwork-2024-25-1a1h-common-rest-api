import os

env = os.getenv("FLASK_ENV", "development")


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    MAIN_DATABASE_1A_URL = os.getenv("MAIN_DATABASE_1A_URL", "https://allenamento1a2025-default-rtdb.firebaseio.com")
    MAIN_DATABASE_1H_URL = os.getenv("MAIN_DATABASE_1H_URL", "https://passaggiolivello-2ffe6-default-rtdb.firebaseio.com")
    REST_API_URL = os.getenv("REST_API_URL", "http://127.0.0.1:5010")

    # JSON credentials-file based configuration:
    MAIN_DATABASE_1A_CREDENTIALS = os.getenv("MAIN_DATABASE_1A_CREDENTIALS", "creds/allenamento1a2025-firebase-adminsdk-fbsvc-866d687579.json")
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
    MAIN_DATABASE_1A_URL = os.getenv("MAIN_DATABASE_1A_URL", "https://allenamento1a2025-default-rtdb.firebaseio.com")
    MAIN_DATABASE_1H_URL = os.getenv("MAIN_DATABASE_1H_URL", "https://passaggiolivello-2ffe6-default-rtdb.firebaseio.com")
    REST_API_URL = os.getenv("REST_API_URL", "http://127.0.0.1:5010")

    # JSON credentials-file based configuration:
    MAIN_DATABASE_1A_CREDENTIALS = os.getenv("MAIN_DATABASE_1A_CREDENTIALS", "creds/allenamento1a2025-firebase-adminsdk-fbsvc-866d687579.json")
    MAIN_DATABASE_1H_CREDENTIALS = os.getenv("MAIN_DATABASE_1H_CREDENTIALS", "creds/passaggiolivello-2ffe6-firebase-adminsdk-fbsvc-93607d7cea.json")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig

}
