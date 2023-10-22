import logging


class LevelFilter(logging.Filter):  # TODO: Docstring
    """
    https://stackoverflow.com/a/7447596/190597 (robert)
    """
    level = None

    def __init__(self, level=0):  # TODO: Docstring
        self.level = level

    def filter(self, record):  # TODO: Docstring
        return record.levelno >= self.level
