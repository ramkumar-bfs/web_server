# Default Party Imports
# TODO: Replace this with environment module, Dont use os to load env
import os
from pathlib import Path
from http.server import HTTPServer

# Local Imports
from ..exceptions import ServerValidationException
from ..server import ModuleRequestHandler
from .. import constants as CONSTANTS

# Modlue Level Constants
_STATIC_FILE_ROOT_DIRECTORY = Path(__file__).parent / "static"


def _get_static_file_content_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".js"):
        return "application/javascript"
    elif filename.endswith(".png"):
        return "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    else:
        return "application/octet-stream"


def _get_static_file_path(filename):
    file_path = _STATIC_FILE_ROOT_DIRECTORY / filename

    if file_path.exists() and file_path.is_file():
        return file_path
    else:
        # TODO: Define proper exception for static file not found
        raise FileNotFoundError(f"Static file '{filename}' not found.")


def _get_static_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def _get_unsupported_application_methods(application_supported_methods):
    """"""
    if not isinstance(application_supported_methods, list):
        raise ServerValidationException(
            f"Provided Application Methods should a 'List' dataType, But got '{type(application_supported_methods)}'"
        )

    return [
        method
        for method in application_supported_methods
        if method not in CONSTANTS.SERVER_SUPPORTED_METHODS
    ]


def get_static_file(filename):
    # TODO: Handle or send Exception response to client
    status = 200
    try:
        content_type = _get_static_file_content_type(filename)
        file_path = _get_static_file_path(filename)
        content = _get_static_content(file_path)
    except FileNotFoundError as exc:
        status = 404
        # TODO: Define proper exception for static file not found in static files
        # TODO: Remove the hardcoded HTML 404 response
        content_type = "text/html"
        content = b"<html><body><h1>404 Not Found</h1></body></html>"

    return status, content_type, content


def get_application_endpoints(application_handlers):
    """ """
    # Validate application handlers
    validate_application_handlers(application_handlers)
    return [
        endpoint
        for method_handlers in application_handlers.values()
        for endpoint in method_handlers.keys()
    ]


def validate_application_handlers(application_handlers):
    """ """
    if not isinstance(application_handlers, dict):
        raise ServerValidationException(
            f"Application Handlers should a 'dict' of 'endpoints' keys with 'functionObject' values. Not '{type(application_handlers)}' datatype provided."
        )

    # Validate Methods in application handlers
    unsupported_methods = _get_unsupported_application_methods(
        list(application_handlers.keys())
    )

    if unsupported_methods:
        raise ServerValidationException(
            f"The following Methods '{' , '.join(unsupported_methods)}'are not supported by WebServer"
        )

    handlers_validate_mapper = {
        handler.__name__: handler
        for endpoint_mapper in application_handlers.values()
        for handler in endpoint_mapper.values()
    }

    if not all(handlers_validate_mapper.values()):
        raise ServerValidationException(
            f"The following Handlers are not callable '{' , '.join([handler_name for handler_name, is_callable in handlers_validate_mapper if not is_callable])}', Validate application handlers."
        )


def run_server():
    # TODO: REPLACE WITH GET_ENV FUNCTION FOR ENVIRONMENT MODULE
    web_server_url = os.environ[CONSTANTS.WEB_SERVER_HOST]
    web_server_port = int(os.environ[CONSTANTS.WEB_SERVER_PORT])
    server_address = (web_server_url, web_server_port)
    httpd = HTTPServer(server_address, ModuleRequestHandler)
    # TODO: Dont use Print statement , Use CUSTOM Logging Module not logging module
    print(f"Hosting WebServer at 'http://{web_server_url}:{web_server_port}'")
    print("Running Server...")
    httpd.serve_forever()
