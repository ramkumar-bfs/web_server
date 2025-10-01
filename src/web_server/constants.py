# Local Imports
# TODO: Do not import any modules inside constants. Get_handlers to str imports
from .api import handlers

WEB_SERVER_HOST = "WEB_SERVER_HOST"
WEB_SERVER_PORT = "WEB_SERVER_PORT"

# API ENDPOINT MAPPER
API_FUNCTION_MAPPER = {
    "GET": {"/api/hello": handlers.hello_handler, "/api/current_time": handlers.time_handler},
    "POST": {"/api/echo": handlers.echo_handler, "/api/sum": handlers.sum_handler},
    "PUT": {},
    "DELETE": {},
}
