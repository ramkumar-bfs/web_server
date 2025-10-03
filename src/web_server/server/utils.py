from http.server import HTTPServer
from pathlib import Path
from collections import namedtuple
from .server import ModuleRequestHandler
from .. import constants as CONSTANTS
from ..environment import get_env
from ..logger import log_info

STATIC_FILE_ROOT = Path(__file__).parent / "static"
StaticFileResponse = namedtuple("StaticFileResponse", ["status", "content_type", "content"])


def _get_static_file_content_type(filename):
    """"""
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
    """"""
    file_path = STATIC_FILE_ROOT / filename
    if file_path.exists() and file_path.is_file():
        return file_path
    raise FileNotFoundError(f"Static file '{filename}' not found.")


def _load_default_404():
    """"""
    file_path = STATIC_FILE_ROOT / "404.html"
    return file_path.read_bytes() if file_path.exists() else b"<html><body><h1>404 Not Found</h1></body></html>"


def get_static_file(filename):
    """"""
    try:
        content_type = _get_static_file_content_type(filename)
        file_path = _get_static_file_path(filename)
        content = file_path.read_bytes()
        return StaticFileResponse(200, content_type, content)
    except FileNotFoundError:
        return StaticFileResponse(404, "text/html", _load_default_404())


def run_server(api_handler=None, host=None, port=None):
    """"""
    if host is None:
        host = get_env(CONSTANTS.WEB_SERVER_HOST)
    if port is None:
        port = int(get_env(CONSTANTS.WEB_SERVER_PORT))

    # Assign the API handler to the request handler class before creating the server
    if api_handler is not None:
        ModuleRequestHandler.api_handler = api_handler

    server_address = (host, port)
    httpd = HTTPServer(server_address, ModuleRequestHandler)

    log_info(f"Hosting WebServer at 'http://{host}:{port}'")
    log_info("Running Server...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log_info("Server shutting down...")
        httpd.server_close()
