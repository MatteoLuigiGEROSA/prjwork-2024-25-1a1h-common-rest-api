from flask import Flask
import logging
import os
from utils.config import config, env

def get_logger(name: str = "app", level: int = None, mode: str = "cf") -> logging.Logger:
    logger = logging.getLogger(name)

    logs_dir = config[env].LOGS_DIR
    app_name = config[env].FLASK_WEBAPP_NAME

    log_filename = f"{app_name}.log" if app_name is not None else "webapp-server.log"

    # Determina il livello di log ed i canali di output da argomento o da variabile d'ambiente:
    log_level_default = config[env].LOG_LEVEL_ALL_MODULES_DEFAULT
    log_channels_default = config[env].LOG_CHANNELS_ALL_MODULES_DEFAULT

    # Impostazione del livello di log e dei canali di output effettivi:
    effective_mode = mode if mode is not None else log_channels_default
    effective_level = level if level is not None else log_level_default.upper()

    # # DEBUG FOR SET-ENVS:
    # print(f"name .... {name}")
    # print(f"level ... {level}")
    # print(f"mode .... {mode}")
    # print("=====")
    # print(f"effective_level ... {effective_level}")
    # print(f"effective_mode .... {effective_mode}")
    # print("- - -")
    # print(f"logs_dir ....................................... {logs_dir}")
    # print(f"config[env].LOGS_DIR ........................... {config[env].LOGS_DIR}")
    # print("- - -")
    # print(f"app_name ....................................... {app_name}")
    # print(f"config[env].FLASK_WEBAPP_NAME .................. {config[env].FLASK_WEBAPP_NAME}")
    # print(f"log_filename ................................... {log_filename}")
    # print("- - -")
    # print(f"log_level_default .............................. {log_level_default}")
    # print(f"config[env].LOG_LEVEL_ALL_MODULES_DEFAULT ...... {config[env].LOG_LEVEL_ALL_MODULES_DEFAULT}")
    # print("- - -")
    # print(f"log_channels_default ........................... {log_channels_default}")
    # print(f"config[env].LOG_CHANNELS_ALL_MODULES_DEFAULT ... {config[env].LOG_CHANNELS_ALL_MODULES_DEFAULT}")
    # print("=====\n")

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt='#### <%(asctime)s> <%(levelname)s> <%(name)s> <%(module)s> <%(threadName)s> <%(message)s>',
            datefmt='%b %d, %Y %I:%M:%S %p'
        )

        if 'c' in effective_mode:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        if 'f' in effective_mode:
            os.makedirs(logs_dir, exist_ok=True)
            log_file = os.path.join(logs_dir, log_filename)  # Central log file
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        logger.setLevel(getattr(logging, effective_level, logging.INFO))
        logger.propagate = False

    return logger


# def get_logger(name: str = "app", level: int = logging.INFO, mode: str = "c") -> logging.Logger:
#     logger = logging.getLogger(name)

#     if not logger.handlers:
#         formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')

#         if 'c' in mode:
#             ch = logging.StreamHandler()
#             ch.setFormatter(formatter)
#             logger.addHandler(ch)

#         if 'f' in mode:
#             log_dir = "logs"
#             os.makedirs(log_dir, exist_ok=True)
#             fh = logging.FileHandler(os.path.join(log_dir, f"{name}.log"), encoding="utf-8")
#             fh.setFormatter(formatter)
#             logger.addHandler(fh)

#         logger.setLevel(level)
#         logger.propagate = False

#     return logger
