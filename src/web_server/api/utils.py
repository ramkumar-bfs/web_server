# Default Imports
import json


# Local Imports
from ..constants import API_FUNCTION_MAPPER
from ..exceptions import WebServerException, APIException


# TODO: Need to implement server logging and monitoring
# TODO: Add authentication and authorization for API endpoints
# TODO: Implement rate limiting and request throttling
# TODO: Add support for HTTPS and secure connections
# TODO: Add unit tests and integration tests for API handlers
# TODO: Implement Server response for exception scenarios


def _raise_api_exception(method, path, parent_exception=None):
    """"""
    exception_msg = f"'{path}' HTTP '{method}' api endpoint not implemented."
    if parent_exception:
        raise WebServerException(exception_msg) from parent_exception

    raise WebServerException(exception_msg)


def _get_api_handler(method, path):
    """"""
    if method not in API_FUNCTION_MAPPER.keys():
        raise WebServerException(f"HTTP Method '{method}' not Implemented.")

    api_handler = API_FUNCTION_MAPPER[method].get(path)
    if not api_handler:
        _raise_api_exception(method, path)

    return api_handler


def execute_api_handler(method, path, data=None):
    """"""
    try:
        handler = _get_api_handler(method, path)
    except WebServerException as exc:
        # TODO: Add logging and Exception response to client
        raise WebServerException("Failed to get API handler.") from exc
    # Execute handler and get response
    if data:
        response = handler(payload=data)
    else:
        response = handler()
    if not isinstance(response, dict):
        # TODO: Define proper exception for API response errors
        # TODO: Add logging for invalid response types
        # TODO: Implement error response to client
        raise APIException("API handler must return a dictionary response.")

    # TODO: Define proper response structure
    return 200, "application/json", json.dumps(response).encode()
