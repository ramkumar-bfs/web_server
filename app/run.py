from web_server.server.utils import run_server
from api import execute_api_handler

if __name__ == "__main__":
    run_server(api_handler=execute_api_handler, host="localhost", port=8080)
