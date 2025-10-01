# Local Imports
# TODO: Do not import any modules inside constants. check to str imports
from . import api

WEB_SERVER_HOST = "WEB_SERVER_HOST"
WEB_SERVER_PORT = "WEB_SERVER_PORT"

# API ENDPOINT MAPPER
API_FUNCTION_MAPPER = {
    "GET": {"/api/hello": api.hello_handler, "/api/current_time": api.time_handler},
    "POST": {"/api/echo": api.echo_handler, "/api/sum": api.sum_handler},
    "PUT": {},
    "DELETE": {},
}
