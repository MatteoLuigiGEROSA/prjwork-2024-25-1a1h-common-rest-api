from functools import wraps
from flask import request, current_app
from utils.tracing.logger_utils import get_logger
from utils.config import config, env
import time

# Logger per le invocazioni REST API:
logger_name = "restful_api"
config_logger_level = config[env].RESTFUL_API_LOGGER_LOG_LEVEL
config_logger_mode = config[env].RESTFUL_API_LOGGER_LOG_CHANNELS

logger = get_logger(name=logger_name, level=config_logger_level, mode=config_logger_mode)

def log_restful_method_call_standalone(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        method = request.method
        path = request.path
        ip = request.remote_addr
        req_payload = request.get_json(silent=True) or request.form.to_dict()

        try:
            app_name = current_app.name
        except RuntimeError:
            app_name = "CommonRestApi"

        logger.info(f"#### <{time.strftime('%b %d, %Y %H:%M:%S')}> <{method}> <RESTfulCall> <{ip}> <{path}> <Request>")
        logger.debug(f"Request Payload: {req_payload}")

        start = time.perf_counter()
        try:
            response = func(*args, **kwargs)
            res_payload = response
            return response
        finally:
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"#### <{time.strftime('%b %d, %Y %H:%M:%S')}> <{method}> <RESTfulCall> <{ip}> <{path}> <Completed in {duration:.2f} ms>")
            logger.debug(f"Response Payload: {res_payload}")

    return wrapper


def log_restful_method_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        method = request.method
        path = request.path
        ip = request.remote_addr
        req_payload = request.get_json(silent=True) or request.form.to_dict()

        try:
            app_name = current_app.name
        except RuntimeError:
            app_name = "CommonRestApi"

        logger.info(f"REST-INVOCATION-DETAILS <{time.strftime('%b %d, %Y %H:%M:%S')}> <{method}> <RESTfulCall> <{ip}> <{path}> <Request>")
        logger.debug(f"Request Payload: {req_payload}")

        start = time.perf_counter()
        try:
            response = func(*args, **kwargs)
            res_payload_and_return_code = response
            return response
        finally:
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"REST-INVOCATION-DETAILS <{time.strftime('%b %d, %Y %H:%M:%S')}> <{method}> <RESTfulCall> <{ip}> <{path}> <Completed in {duration:.2f} ms>")
            logger.debug(f"Response Payload and Return-Code: {res_payload_and_return_code}")

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


# logger = get_logger("restful_api", mode="cf")

# def log_restful_method_call(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         method = request.method
#         path = request.path
#         ip = request.remote_addr
#         payload = request.get_json(silent=True) or request.form.to_dict()
#         logger.info(f"[{method}] {path} - IP: {ip}")
#         logger.debug(f"Payload: {payload}")

#         start = time.perf_counter()
#         response = func(*args, **kwargs)
#         duration = (time.perf_counter() - start) * 1000
#         logger.info(f"[{method}] {path} - Completato in {duration:.2f} ms")

#         return response
#     return wrapper

# def log_restful_class_on_any_method_call(decorator):
#     """
#     Applica un decoratore a tutti i metodi HTTP di una classe Resource.
#     """
#     def decorate(cls):
#         for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
#             if hasattr(cls, method):
#                 original = getattr(cls, method)
#                 setattr(cls, method, decorator(original))
#         return cls
#     return decorate
