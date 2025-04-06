import time
from functools import wraps
from utils.config import config, env
from utils.tracing.logger_utils import get_logger

# Logger centralizzato per tutte le operazioni RESTful e Firebase
logger_name = "firebase_ops"
config_logger_level = config[env].FIREBASE_OPS_LOGGER_LOG_LEVEL
config_logger_mode = config[env].FIREBASE_OPS_LOGGER_LOG_CHANNELS

logger = get_logger(name=logger_name, level=config_logger_level, mode=config_logger_mode)

def log_firebase_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = getattr(args[0], '_path', '/') if hasattr(args[0], '_path') else kwargs.get("path", "/")
        method_name = func.__name__

        logger.info(f"DATABASE-INVOCATION-DETAILS <{time.strftime('%b %d, %Y %H:%M:%S')}> <FIREBASE> <{method_name}> <{path}> <Start>")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"DATABASE-INVOCATION-DETAILS <{time.strftime('%b %d, %Y %H:%M:%S')}> <FIREBASE> <{method_name}> <{path}> <Completed in {duration:.2f} ms>")
            return result
        except Exception as e:
            logger.error(f"DATABASE-INVOCATION-DETAILS <{time.strftime('%b %d, %Y %H:%M:%S')}> <FIREBASE> <{method_name}> <{path}> <Errore: {e}>")
            raise
    return wrapper


# logger = get_logger("firebase_ops", mode="cf")

# def log_firebase_operation(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         path = getattr(args[0], '_path', '/') if hasattr(args[0], '_path') else kwargs.get("path", "/")
#         method_name = func.__name__
#         logger.info(f"[FIREBASE] Operazione: {method_name} - Path: {path}")
#         start = time.perf_counter()
#         try:
#             result = func(*args, **kwargs)
#             duration = (time.perf_counter() - start) * 1000
#             logger.info(f"[FIREBASE] {method_name} completato in {duration:.2f} ms")
#             return result
#         except Exception as e:
#             logger.error(f"[FIREBASE] Errore in {method_name} su path '{path}': {e}")
#             raise
#     return wrapper
