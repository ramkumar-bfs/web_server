from http.server import BaseHTTPRequestHandler

class ModuleRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler. Delegates actual logic to external API handler."""

    # This will be injected by the app
    api_handler = None

    def _send_content(self, code, content_type, message=None):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if message:
            if isinstance(message, str):
                self.wfile.write(message.encode("utf-8"))
            elif isinstance(message, bytes):
                self.wfile.write(message)

    def _send_html_content(self, code, message=None):
        self._send_content(code, "text/html", message)

    def _send_json_content(self, code, message=None):
        self._send_content(code, "application/json", message)

    def _get_post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length).decode("utf-8")

    def _do(self, method):
        if not self.api_handler:
            self._send_json_content(500, '{"error": "API handler not set"}')
            return

        post_data = None
        if method in ["POST", "PUT", "PATCH", "DELETE"]:
            post_data = self._get_post_data()

        # Call the injected API handler
        print(f"Calling API handler for {method} {self.path} with data: {post_data}")
        print(f"API handler: {self.api_handler}")
        status, content_type, content = self.api_handler(method, self.path, post_data)

        if content_type == "text/html":
            self._send_html_content(status, content)
        elif content_type == "application/json":
            self._send_json_content(status, content)
        else:
            self._send_content(status, content_type, content)

    def do_GET(self): self._do("GET")
    def do_POST(self): self._do("POST")
    def do_PUT(self): self._do("PUT")
    def do_DELETE(self): self._do("DELETE")
    def do_PATCH(self): self._do("PATCH")
    def do_OPTIONS(self): self._do("OPTIONS")
    def do_HEAD(self): self._do("HEAD")
