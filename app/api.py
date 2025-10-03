import json


def execute_api_handler(method, path, data=None):
    """"""
    # method: HTTP method as string e.g., "GET", "POST"
    # path: requested URL path as string
    # data: POST data or None
    print(f"Executing API handler for {method} {path} with data: {data}")

    if path == "/api/hello" and method == "GET":
        return 200, "application/json", json.dumps({"message": "Hello!"})

    elif path == "/api/echo" and method == "POST":
        return 200, "application/json", json.dumps({"echo": data})

    return 404, "application/json", json.dumps({"error": "Not Found"})
