class WebServerException(Exception):
    """Base exception for web server errors."""

    pass


class APIException(WebServerException):
    """Exception for API related errors."""

    pass
