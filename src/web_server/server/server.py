# Default Imports
from http.server import BaseHTTPRequestHandler

# Local Imports
from ..api import utils
from .. import static

# NOTE: This class by default support all do_<api_method> meathods if not implementeded, Raises 501 ERROR
class ModuleRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            status, content_type, content = static.get_static_file("index.html")
        elif self.path.startswith("/static/"):
            filename = self.path[len("/static/") :]
            status, content_type, content = static.get_static_file(filename)
        else:
            result = utils.handle_api_get(self.path)
            if result is not None:
                status, content_type, content = result
            else:
                self.send_error(404, "Not Found")
                return
        self._set_headers(status, content_type)
        self.wfile.write(content)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        result = utils.handle_api_post(self.path, post_data)
        if result is not None:
            status, content_type, content = result
            self._set_headers(status, content_type)
            self.wfile.write(content)
        else:
            self.send_error(404, "Not Found")
