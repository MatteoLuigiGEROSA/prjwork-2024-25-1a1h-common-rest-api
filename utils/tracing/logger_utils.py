import logging
import os

def get_logger(name: str = "app", level: int = logging.INFO, mode: str = "c") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')

        if 'c' in mode:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        if 'f' in mode:
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            fh = logging.FileHandler(os.path.join(log_dir, f"{name}.log"), encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        logger.setLevel(level)
        logger.propagate = False

    return logger
