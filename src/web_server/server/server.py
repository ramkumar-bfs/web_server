# Default Imports
from http.server import BaseHTTPRequestHandler

# Local Imports
from ..api import utils


# NOTE: This class by default support all do_<api_method> meathods if not implementeded, Raises 501 ERROR
class ModuleRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler for handling API requests."""

    def _send_content(self, code, content_type, message=None):
        """Send HTTP response with given status code and message."""
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if message:
            if isinstance(message, str):
                self.wfile.write(message.encode("utf-8"))
            elif isinstance(message, bytes):
                self.wfile.write(message)

    def _send_html_content(self, code, message=None):
        """Send HTTP response with given status code and message."""
        self._send_content(code, "text/html", message)

    def _send_json_content(self, code, message=None):
        """Send HTTP response with given status code and message."""
        self._send_content(code, "application/json", message)

    def _get_post_data(self):
        """Read and return the POST data from the request."""
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length).decode("utf-8")

    def _do(self, method):
        """Handle HTTP requests by executing the appropriate API handler."""
        post_data = None
        if method == "POST":
            post_data = self._get_post_data()

        status, content_type, content = utils.execute_api_handler(
            "GET", self.path, data=post_data
        )

        if content_type == "text/html":
            self._send_html_content(status, content)
        elif content_type == "application/json":
            self._send_json_content(status, content)

    def do_GET(self):
        """Handle GET requests."""
        self._do("GET")

    def do_POST(self):
        """Handle POST requests."""
        self._do("POST")
