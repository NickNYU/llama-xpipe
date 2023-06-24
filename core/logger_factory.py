import logging
from logging import handlers
from typing import Optional


def get_logger(name: [str],
               file_name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if file_name is None:
        file_name = 'app-default.log'
    handler = handlers.TimedRotatingFileHandler(filename=file_name,
                                                when='d',
                                                backupCount=21,
                                                encoding='UTF-8')
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(message)s]')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # Configure the logger as desired
    # e.g., add handlers, set log levels, etc.
    return logger
