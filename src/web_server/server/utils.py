# Default Party Imports
# TODO: Replace this with environment module, Dont use os to load env
import os
from pathlib import Path
from http.server import HTTPServer

# Local Imports
from .server import ModuleRequestHandler
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
        # TODO: Remove the handcoded HTML 404 response
        content_type = "text/html"
        content = b"<html><body><h1>404 Not Found</h1></body></html>"

    return status, content_type, content


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
