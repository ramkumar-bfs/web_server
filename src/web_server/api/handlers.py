# Local Imports
from datetime import datetime


# Define GET endpoints
def favicon_handler():
    """"""
    # TODO: Serve actual favicon file
    return {"message": "PIPELINE FAVICON"}


# TODO: Seprate appilcation apis into different modules like appilcation, user, auth etc
def hello_handler():
    """"""
    return {"message": "Hello from the API!"}


def time_handler():
    """"""
    return {"time": datetime.now().isoformat()}


# Define POST endpoints
def echo_handler(payload):
    """"""
    return {"received": payload}


def sum_handler(payload):
    """"""
    numbers = payload.get("numbers", [])
    total = sum(numbers) if isinstance(numbers, list) else 0
    return {"sum": total}
