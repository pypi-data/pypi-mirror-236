class Loglevel:  # TODO: Docstring
    STRING: str = 'NOTSET'
    INT: int = 0


class NOTSET(Loglevel):  # TODO: Docstring
    STRING: 'NOTSET'
    INT: 0


class DEBUG(Loglevel):  # TODO: Docstring
    STRING: str = 'DEBUG'
    INT: int = 10


class INFO(Loglevel):  # TODO: Docstring
    STRING: str = 'INFO'
    INT: int = 20


class WARNING(Loglevel):  # TODO: Docstring
    STRING: str = 'WARNING'
    INT: int = 30


class ERROR(Loglevel):  # TODO: Docstring
    STRING: str = 'ERROR'
    INT: int = 40


class CRITICAL(Loglevel):  # TODO: Docstring
    STRING: str = 'CRITICAL'
    INT: int = 50
