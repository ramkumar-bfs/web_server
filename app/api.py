import json

def execute_api_handler(*args, **kwargs):
    print(f"Args: {args}, Kwargs: {kwargs}")

    if len(args) < 3:
        return 400, "application/json", json.dumps({"error": "Insufficient arguments"})

    # Skip the first arg (self/request handler)
    method = args[1]
    path = args[2]
    data = args[3] if len(args) > 3 else None

    # Now dispatch based on method and path
    if path == "/" and method == "GET":
        return 200, "application/json", json.dumps({"message": "welcome to the home page!"})

    elif path == "/api/hello" and method == "GET":
        return 200, "application/json", json.dumps({"message": "Hello from GET!"})
    
    elif path == "/api/echo" and method == "POST":
        return 200, "application/json", json.dumps({"echo": data})

    elif path == "/api/update" and method == "PUT":
        return 200, "application/json", json.dumps({"status": "Updated", "data": data})

    elif path == "/api/modify" and method == "PATCH":
        return 200, "application/json", json.dumps({"status": "Modified", "data": data})

    elif path == "/api/delete" and method == "DELETE":
        return 200, "application/json", json.dumps({"status": "Deleted"})

    elif path == "/api/options" and method == "OPTIONS":
        return 200, "application/json", json.dumps({
            "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
        })

    elif path == "/api/head" and method == "HEAD":
        return 200, "application/json", b""

    return 404, "application/json", json.dumps({"error": f"No handler for {method} {path}"})
