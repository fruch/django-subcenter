# stdlib
import threading
import logging
# django
from django.conf import settings
import imdb
#===============================================================================
# Globals
#===============================================================================
_LOCALS = threading.local()

def get_logger():
    logger = getattr(_LOCALS, 'logger', None)
    if logger is not None:
        return logger

    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s - %(funcName)s - %(lineno)d - %(message)s','%Y-%m-%d %a %H:%M:%S')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(getattr(settings, 'LOG_LEVEL', logging.NOTSET))
    
    setattr(_LOCALS, 'logger', logger)
    
    imdb._logging.setLevel(getattr(settings, 'LOG_LEVEL', logging.NOTSET))
    
    return logger