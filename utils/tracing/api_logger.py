from functools import wraps
from flask import request
from .logger_utils import get_logger
import time

logger = get_logger("api", mode="cf")

def log_api_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"[API] {request.method} {request.path} - IP: {request.remote_addr}")
        logger.debug(f"[API] Params: {request.args.to_dict() if request.method == 'GET' else request.get_json(silent=True)}")
        start = time.perf_counter()
        response = func(*args, **kwargs)
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"[API] {request.method} {request.path} - Completed in {duration:.2f} ms")
        return response
    return wrapper
