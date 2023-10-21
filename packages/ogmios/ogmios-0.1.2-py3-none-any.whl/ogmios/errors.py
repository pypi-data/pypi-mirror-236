class InvalidMethodError(Exception):
    """Raised when Ogmios response contains an unexpected method name"""

    pass


class InvalidResponseError(Exception):
    """Raised when Ogmios response contains unexpected content"""

    pass


class InvalidBlockParameter(Exception):
    """Raised when missing or invalid parameters are passed to a Block object"""

    pass


class ResponseError(Exception):
    """Raised when an Ogmios request contains an error message"""

    pass
