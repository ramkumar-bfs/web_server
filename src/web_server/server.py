from http.server import BaseHTTPRequestHandler, HTTPServer
from . import api, static


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
            result = api.handle_api_get(self.path)
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
        result = api.handle_api_post(self.path, post_data)
        if result is not None:
            status, content_type, content = result
            self._set_headers(status, content_type)
            self.wfile.write(content)
        else:
            self.send_error(404, "Not Found")


def run(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ModuleRequestHandler)
    print(f"Serving HTTP API and static files on port {port} ...")
    httpd.serve_forever()
