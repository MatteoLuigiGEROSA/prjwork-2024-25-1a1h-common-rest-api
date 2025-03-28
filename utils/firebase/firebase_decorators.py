import time
from functools import wraps
from utils.tracing.logger_utils import get_logger

logger = get_logger("firebase_ops", mode="cf")

def log_firebase_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = getattr(args[0], '_path', '/') if hasattr(args[0], '_path') else kwargs.get("path", "/")
        method_name = func.__name__
        logger.info(f"[FIREBASE] Operazione: {method_name} - Path: {path}")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"[FIREBASE] {method_name} completato in {duration:.2f} ms")
            return result
        except Exception as e:
            logger.error(f"[FIREBASE] Errore in {method_name} su path '{path}': {e}")
            raise
    return wrapper
