from functools import wraps
from flask import request
from .logger_utils import get_logger
import time

logger = get_logger("restful_api", mode="cf")

def log_restful_method_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        method = request.method
        path = request.path
        ip = request.remote_addr
        payload = request.get_json(silent=True) or request.form.to_dict()
        logger.info(f"[{method}] {path} - IP: {ip}")
        logger.debug(f"Payload: {payload}")

        start = time.perf_counter()
        response = func(*args, **kwargs)
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"[{method}] {path} - Completato in {duration:.2f} ms")

        return response
    return wrapper

def log_restful_class_on_any_method_call(decorator):
    """
    Applica un decoratore a tutti i metodi HTTP di una classe Resource.
    """
    def decorate(cls):
        for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
            if hasattr(cls, method):
                original = getattr(cls, method)
                setattr(cls, method, decorator(original))
        return cls
    return decorate
