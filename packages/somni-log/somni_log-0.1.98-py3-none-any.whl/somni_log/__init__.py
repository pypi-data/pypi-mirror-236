import logging
from logging import Logger, debug, info, warning, error, critical
from somni_log.constants import Loglevel, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from somni_log.level_filter import LevelFilter

DEFAULT_LEVEL: Loglevel = INFO
DEFAULT_MESSAGE_FORMAT: str = '%(name)s | %(asctime)s | %(levelname)s | %(filename)s | %(funcName)s() | %(message)s'
DEFAULT_DATETIME_FORMAT: str = '%Y.%m.%d %H:%M:%S'
DEFAULT_CAPITALIZE_LOG_NAME: bool = False
DEFAULT_DEV_MODE: bool = False


def create_logger(name: str, level: Loglevel = DEFAULT_LEVEL,
                  message_format=DEFAULT_MESSAGE_FORMAT, datetime_format=DEFAULT_DATETIME_FORMAT,
                  capitalize_name=DEFAULT_CAPITALIZE_LOG_NAME, dev_mode: bool = DEFAULT_DEV_MODE
                  ) -> Logger:  # TODO:
    if dev_mode:
        level = DEBUG
    if capitalize_name:
        name = name.upper()

    logger = logging.getLogger(name=name.strip())
    logger.setLevel(level=level.STRING)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.addFilter(LevelFilter(level=level.INT))
    stream_handler.setFormatter(logging.Formatter(message_format.strip(), datefmt=datetime_format.strip()))
    logger.addHandler(stream_handler)

    logger.debug(f'Started Logger (Name: {logger.name}, Level: {logger.level}).')
    return logger


class Somni_Log:
    LEVEL: Loglevel = DEFAULT_LEVEL,
    MESSAGE_FORMAT: str = DEFAULT_MESSAGE_FORMAT,
    DATETIME_FORMAT: str = DEFAULT_DATETIME_FORMAT,
    DEV_MODE: bool = DEFAULT_DEV_MODE
    CHILDREN: dict = {}

    @classmethod
    def __init__(cls, level: Loglevel = LEVEL,
                 message_format: str = DEFAULT_MESSAGE_FORMAT,
                 datetime_format: str = DEFAULT_DATETIME_FORMAT,
                 dev_mode: bool = DEFAULT_DEV_MODE
                 ):
        if dev_mode:
            cls.LEVEL = DEBUG
        else:
            cls.LEVEL = level

        cls.MESSAGE_FORMAT = message_format
        cls.DATETIME_FORMAT = datetime_format

        logging.basicConfig(level=cls.LEVEL.STRING, format=cls.MESSAGE_FORMAT.strip())

        logging.debug(
            f'Set up Root-Logger (Dev-mode: {dev_mode}, Level: \'{level}\', '
            f'Message-format: {message_format}, Datetime-format: {datetime_format}).'
        )

    @classmethod
    def create(cls, name: str, level: Loglevel = DEFAULT_LEVEL,
               message_format=DEFAULT_MESSAGE_FORMAT, datetime_format=DEFAULT_DATETIME_FORMAT,
               capitalize_name=DEFAULT_CAPITALIZE_LOG_NAME, dev_mode: bool = DEFAULT_DEV_MODE
               ) -> Logger:
        if name in cls.CHILDREN.keys():
            raise KeyError(f'Logger with identical name already exists!')

        logger = create_logger(name=name, level=level,
                               message_format=message_format, datetime_format=datetime_format,
                               capitalize_name=capitalize_name, dev_mode=dev_mode)
        cls.CHILDREN[name] = logger
        return logger

    # TODO: def suppress message (partly?)

    # TODO: def suppress logging():

    # TODO: def suppress_logger(cls, logger: Logger):
