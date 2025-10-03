from datetime import datetime


def _log(level: str, message: str):
    """
    Internal method to format and print log messages with timestamp.
    :param level: Log level (INFO, ERROR, etc.)
    :param message: The message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")


def log_info(message: str):
    """Log an info message."""
    _log("INFO", message)


def log_warning(message: str):
    """Log a warning message."""
    _log("WARNING", message)


def log_error(message: str):
    """Log an error message."""
    _log("ERROR", message)


def log_debug(message: str):
    """Log a debug message."""
    _log("DEBUG", message)
