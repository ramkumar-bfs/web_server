# test_module_request_handler.py
import threading
import time
import pytest
import requests
from http.server import HTTPServer
from web_server import ModuleRequestHandler

_BASE_URL = "http://localhost:8001"


# -------------------------
# Example Handlers
# -------------------------
def hello_get_handler(pay_load=None):
    return 200, "application/json", {"message": "Hello, GET request received!"}


def echo_post_handler(pay_load=None):
    return 200, "application/json", {"received": pay_load}


def invalid_handler(pay_load=None):
    return {"not", "a", "tuple"}  # Should trigger 500


def error_handler(pay_load=None):
    raise RuntimeError("Handler error!")


handlers = {
    "GET": {
        "/hello": hello_get_handler,
        "/invalid": invalid_handler,
        "/error": error_handler,
    },
    "POST": {"/echo": echo_post_handler},
}


# -------------------------
# Helper function to start server
# -------------------------
@pytest.fixture(scope="module")
def test_server():
    class CustomHandler(ModuleRequestHandler):
        pass

    CustomHandler.name = "ExampleApp"
    CustomHandler.handlers = handlers

    server_address = ("", 8001)  # test on port 8001
    httpd = HTTPServer(server_address, CustomHandler)

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    # Wait a moment for server to start
    time.sleep(0.1)
    yield
    httpd.shutdown()
    thread.join()


# -------------------------
# Tests
# -------------------------
def test_get_hello(test_server):
    url = f"{_BASE_URL}/hello"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = response.json()
    assert data["message"] == "Hello, GET request received!"


def test_post_echo(test_server):
    url = f"{_BASE_URL}/echo"
    payload = {"name": "Ram"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = response.json()
    assert data["received"] == payload


def test_not_found_endpoint(test_server):
    url = f"{_BASE_URL}/notexist"
    response = requests.get(url)
    assert response.status_code == 404
    data = response.json()
    assert "error_msg" in data


def test_method_not_allowed(test_server):
    url = f"{_BASE_URL}/hello"
    response = requests.post(url, json={})
    assert response.status_code == 405
    data = response.json()
    assert "error_msg" in data


def test_not_implemented(test_server):
    resp = requests.put(f"{_BASE_URL}/hello", json={})
    assert resp.status_code == 501 or resp.status_code == 405  # Depending on your logic
    assert "error_msg" in resp.json()


def test_invalid_handler_response(test_server):
    resp = requests.get(f"{_BASE_URL}/invalid")
    assert resp.status_code == 500
    assert "error_msg" in resp.json()


def test_options_cors_headers(test_server):
    resp = requests.options(f"{_BASE_URL}/hello")
    assert resp.status_code == 200
    assert resp.headers["Access-Control-Allow-Origin"] == "*"
    assert "Access-Control-Allow-Methods" in resp.headers
    assert "Access-Control-Allow-Headers" in resp.headers


def test_payload_handling(test_server):
    payload = {"x": 1}
    resp = requests.post(f"{_BASE_URL}/echo", json=payload)
    assert resp.status_code == 200
    assert resp.json()["received"] == payload


def test_payload_invalid_json(test_server):
    resp = requests.post(
        f"{_BASE_URL}/echo",
        data="notjson",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    # Should echo back the raw string since JSON decode fails
    assert resp.json()["received"] == "notjson"
