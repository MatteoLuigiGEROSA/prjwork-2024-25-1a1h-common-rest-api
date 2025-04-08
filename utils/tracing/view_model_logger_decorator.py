from functools import wraps
# import inspect
from utils.config import config, env
from utils.tracing.logger_utils import get_logger

def log_view_model(cls):
    """
    Decoratore di classe per tracciare i parametri in ingresso e uscita dei ViewModel,
    riportandone in modo automatico errori e contenuti.
    """
    # Logger per la valodazione delle classi view-model::
    logger_name = f"viewmodel.{cls.__name__}"
    config_logger_level = config[env].VIEW_MODEL_LOGGER_LOG_LEVEL
    config_logger_mode = config[env].VIEW_MODEL_LOGGER_LOG_CHANNELS

    logger = get_logger(name=logger_name, level=config_logger_level, mode=config_logger_mode)

    original_init = cls.__init__
    original_to_dict = getattr(cls, "to_dict", None)

    def wrapped_init(self, *args, **kwargs):
        logger.debug(f"[{cls.__name__}] Inizializzazione con args={args}, kwargs={kwargs}")
        try:
            original_init(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"[{cls.__name__}] Errore in __init__: {e}", exc_info=True)
            raise

        # Validazione base sui parametri (esempio semplice, si può estendere)
        for name, value in self.__dict__.items():
            if value is None:
                logger.error(f"[{cls.__name__}] ❌ Campo mancante o nullo: '{name}'")
            else:
                logger.debug(f"[{cls.__name__}] ✅ Campo '{name}' = {value}")

    def wrapped_to_dict(self):
        try:
            result = original_to_dict(self)
            logger.debug(f"[{cls.__name__}] Output to_dict(): {result}")
            return result
        except Exception as e:
            logger.error(f"[{cls.__name__}] Errore in to_dict(): {e}", exc_info=True)
            raise

    cls.__init__ = wrapped_init
    if original_to_dict:
        cls.to_dict = wrapped_to_dict

    return cls
