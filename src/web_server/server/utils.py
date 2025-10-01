# Default Party Imports
# TODO: Replace this with environment module, Dont use os to load env
import os
from http.server import HTTPServer

# Local Imports
from .server import ModuleRequestHandler
from .. import constants as CONSTANTS


def run_server():
    # TODO: REPLACE WITH GET_ENV FUNCTION FOR ENVRONMENT MODULE
    web_server_url = os.environ[CONSTANTS.WEB_SERVER_HOST]
    web_server_port = os.environ[CONSTANTS.WEB_SERVER_PORT]
    server_address = (web_server_url, web_server_port)
    httpd = HTTPServer(server_address, ModuleRequestHandler)
    # TODO: Dont use Print statemenet , Use CUSTOM Logging Module not logging module
    print(f"Hosting WebServer at '{web_server_url}:{web_server_port}'")
    print("Running Server...")
    httpd.serve_forever()