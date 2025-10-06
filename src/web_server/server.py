# Default Imports
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# Package Imports
from . import constants as CONSTANTS

# Local Imports
from .exceptions import WebServerException
from .utils import application_utils, server_utils


# NOTE: This class by default support all do_<api_method> methods if not implemented, Raises 501 ERROR
class ModuleRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler for handling API requests."""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        # Property variable
        self._application_handlers = None
        self._application_name = None

    @property
    def name(self):
        """"""
        return self._application_name

    @name.setter
    def name(self, value):
        """"""
        self._application_name = value

    @property
    def handlers(self):
        """ """
        return self._application_handlers

    @handlers.setter
    def handlers(self, value):
        """"""
        # Validate application handlers
        server_utils.validate_application_handlers(value)
        self._application_handlers = value

    def _execute_handler(self, method, endpoint, pay_load=None):
        """ """
        application_endpoint = server_utils.get_application_endpoints(self.handlers)

        if endpoint not in application_endpoint:
            error_msg = f"'{endpoint}' endpoint not found in '{self.name}' Application."
            return application_utils.handle_exception(
                404, WebServerException.__name__, error_msg
            )

        is_method_valid = self.handlers.get(method)
        error_code = error_type = error_msg = None

        if not is_method_valid:
            error_msg = f"'{self.name}' Application doesn't support '{method}' method."
            return application_utils.handle_exception(
                501, WebServerException.__name__, error_msg
            )

        if endpoint not in self.handlers[method]:
            error_msg = f"'{endpoint}' endpoint doesn't support '{method}' method."
            return application_utils.handle_exception(
                405, WebServerException.__name__, error_msg
            )
        handler = self.handlers[method][endpoint]
        try:
            result = handler(pay_load=pay_load) if pay_load else handler()
        # NOTE: Un-Handled exception from application
        except Exception as exc:
            return application_utils.handle_exception(
                500,
                WebServerException.__name__,
                (
                    f"Unhandled exception occurred in '{self.name}' application on "
                    f"'{endpoint}' endpoint for '{method}' method.\n"
                    f"Please check the implementation of '{handler.__name__}'.\n"
                    f"For more info, refer to traceback:\n{exc}"
                ),
            )

        if not isinstance(result, (tuple, list)) or len(result) != 3:
            return application_utils.handle_exception(
                500,
                WebServerException.__name__,
                f"Invalid handler response from {endpoint}",
            )

        status, content_type, content = result
        return status, content_type, content

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_content(self, code, content_type, body=None):
        """Send HTTP response with given status code and body."""
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        elif isinstance(body, bytes):
            body = body or b""
        else:
            body = b""

        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()

        if body:
            self.wfile.write(body)

    def _get_pay_load(self):
        """Extract and return JSON payload from the request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if not content_length:
            return None
        raw = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def _do(self, method):
        """Handle HTTP requests."""
        endpoint = urlparse(self.path).path
        pay_load = (
            self._get_pay_load()
            if method in CONSTANTS.PAYLOAD_REQUIRED_METHODS
            else None
        )

        try:
            status, content_type, content = self._execute_handler(
                method, endpoint, pay_load
            )
        except Exception as e:
            status, content_type, content = application_utils.handle_exception(
                500, type(e).__name__, str(e)
            )

        content_type = content_type or "application/json"
        self._send_content(status, content_type, content)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        self._do("GET")

    def do_POST(self):
        """Handle POST requests."""
        self._do("POST")

    def do_PUT(self):
        """Handle PUT requests."""
        self._do("PUT")

    def do_PATCH(self):
        """Handle Patch requests"""
        self._do("PATCH")

    def do_DELETE(self):
        """Handle DELETE requests"""
        self._do("DELETE")
