import logging
import sys
import time
from os.path import splitext, basename


def __configure_default_logger(logger: logging.Logger) -> None:
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        log_formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)-8s > %(name)-4s : %(message)s')
        log_formatter.converter = time.gmtime

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(log_formatter)

        logger.addHandler(console_handler)


def get_default_logger(log_as: str = None) -> logging.Logger:
    if log_as is None:
        logger = logging.getLogger(splitext(basename(sys.argv[0]))[0])
    else:
        logger = logging.getLogger(log_as)

    __configure_default_logger(logger)

    return logger
