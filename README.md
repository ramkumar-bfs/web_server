# Python Modular Web Server

A modular, extensible Python web server for building custom HTTP APIs and serving static files.  
Supports dynamic handler registration, robust error handling, and is designed for easy testing and extension.

---

## 📦 Features

- Custom HTTP request handler (`ModuleRequestHandler`) for all standard HTTP methods
- Dynamic dispatch to application-defined endpoint handlers
- Automatic JSON error responses for 404, 405, 501, and 500 errors
- Static file serving from the `static/` directory with content-type detection
- Utilities for handler validation, error formatting, and server management
- Easily extensible for authentication, logging, rate limiting, and more

---

## 🏗️ Project Structure

```
src/
  web_server/
    __init__.py
    __main__.py
    constants.py
    exceptions.py
    server.py
    static/
      .gitkeep
    utils/
      __init__.py
      application_utils.py
      server_utils.py
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd web_server
```

### 2. Install Requirements

If you have dependencies, install them (add to `requirements.txt` if needed):

```sh
pip install -r requirements.txt
```

---

## ⚙️ Setting Environment Variables

Before running the server, set the environment variables from your `.env` file:

On **Windows** (Command Prompt):

```sh
set WEB_SERVER_HOST=127.0.0.1
set WEB_SERVER_PORT=8000
set PYTHONPATH=C:\Users\Ramkumar.E\Documents\web_server\src
```

On **Linux/macOS** (Bash):

```sh
export WEB_SERVER_HOST="127.0.0.1"
export WEB_SERVER_PORT=8000
```

You can also use tools like [`python-dotenv`](https://pypi.org/project/python-dotenv/) to load these automatically.

---

### 3. Run the Server

From the `src` directory, run:

```sh
python -m web_server
```

Or, if you have an entrypoint script, use:

```sh
python src/web_server/__main__.py
```

The server will start on the default port (e.g., 8000 or as configured).

---

## 🧩 Registering Handlers

You can define your own handlers and assign them to the server.  
Example:

```python
from web_server.server import ModuleRequestHandler

def hello_handler(payload=None):
    return 200, "application/json", {"message": "Hello, World!"}

class MyHandler(ModuleRequestHandler):
    name = "MyApp"
    handlers = {
        "GET": {"/hello": hello_handler}
    }

# Then use MyHandler in your server setup
```

---

## 🗂️ Serving Static Files

Place your static files (HTML, CSS, JS, images, etc.) in the `src/web_server/static/` directory.  
Access them via `http://localhost:<port>/static/<filename>`.

---

## 🧪 Running Tests

Tests are located in the `tests/` directory.

To run all tests:

```sh
pytest
```

Make sure the server is **not** running on the same port as the tests.

---

## ⚙️ Configuration

- **Port and host** can be set in your server runner or by modifying the server startup code.
- **Supported HTTP methods** and endpoints are defined in your handler class.

---

## 🛠️ Extending

- Add authentication, logging, rate limiting, etc., by extending `ModuleRequestHandler` or using middleware patterns.
- Add more static file types by editing `_get_static_file_content_type` in `server_utils.py`.

---

## ❗ Error Handling

All errors return JSON responses with `error_code`, `error_type`, and `error_msg`.

---

## 📄 License

MIT License (or specify your license here)

---

## 🤝 Contributing

Pull requests and issues are welcome! Please add tests for new features and bug fixes.

---

## 📞 Support

For questions or support, open an issue or contact the maintainer.
