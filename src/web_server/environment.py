import os

from .exceptions import EnvironmentError


def get_env(key: str, default: str = None, required: bool = False) -> str:
    """
    Retrieves an environment variable with optional default and required flag.

    :param key: Name of the environment variable
    :param default: Default value if env var not set
    :param required: If True and env var not set, raises error
    :return: Value of environment variable
    """
    value = os.environ.get(key, default)

    if required and value is None:
        raise EnvironmentError(f"Required environment variable '{key}' is missing.")

    return value
