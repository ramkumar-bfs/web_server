# 3rd Party Imports
import pytest

# Custom Imports
from web_server.utils import server_utils
from web_server.exceptions import ServerValidationException


def test_get_static_file_content_type():
    assert server_utils._get_static_file_content_type("index.html") == "text/html"
    assert server_utils._get_static_file_content_type("style.css") == "text/css"
    assert (
        server_utils._get_static_file_content_type("script.js")
        == "application/javascript"
    )
    assert server_utils._get_static_file_content_type("image.png") == "image/png"
    assert server_utils._get_static_file_content_type("photo.jpg") == "image/jpeg"
    assert (
        server_utils._get_static_file_content_type("unknown.xyz")
        == "application/octet-stream"
    )


def test_get_static_file_path_and_content(tmp_path):
    # Create a temporary static file
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    file_path = static_dir / "test.txt"
    file_path.write_bytes(b"hello world")

    # Patch the _STATIC_FILE_ROOT_DIRECTORY to our temp dir
    orig_dir = server_utils._STATIC_FILE_ROOT_DIRECTORY
    server_utils._STATIC_FILE_ROOT_DIRECTORY = static_dir
    try:
        found_path = server_utils._get_static_file_path("test.txt")
        assert found_path == file_path
        content = server_utils._get_static_content(found_path)
        assert content == b"hello world"
    finally:
        server_utils._STATIC_FILE_ROOT_DIRECTORY = orig_dir


def test_get_static_file_not_found():
    with pytest.raises(FileNotFoundError):
        server_utils._get_static_file_path("doesnotexist.txt")


def test_get_static_file(tmp_path):
    static_dir = tmp_path / "static"
    static_dir.mkdir()
    file_path = static_dir / "test.html"
    file_path.write_bytes(b"<h1>Hi</h1>")

    orig_dir = server_utils._STATIC_FILE_ROOT_DIRECTORY
    server_utils._STATIC_FILE_ROOT_DIRECTORY = static_dir
    try:
        status, content_type, content = server_utils.get_static_file("test.html")
        assert status == 200
        assert content_type == "text/html"
        assert content == b"<h1>Hi</h1>"

        status, content_type, content = server_utils.get_static_file("notfound.html")
        assert status == 404
        assert content_type == "text/html"
        assert b"404 Not Found" in content
    finally:
        server_utils._STATIC_FILE_ROOT_DIRECTORY = orig_dir


def test_get_application_endpoints():
    handlers = {
        "GET": {"/a": lambda: None, "/b": lambda: None},
        "POST": {"/c": lambda: None},
    }
    endpoints = server_utils.get_application_endpoints(handlers)
    assert set(endpoints) == {"/a", "/b", "/c"}


def test__get_unsupported_application_methods():
    from web_server import constants as CONSTANTS

    supported = CONSTANTS.SERVER_SUPPORTED_METHODS
    assert server_utils._get_unsupported_application_methods(supported) == []
    with pytest.raises(ServerValidationException):
        server_utils._get_unsupported_application_methods("notalist")

    assert server_utils._get_unsupported_application_methods(["GET", "FOO"]) == ["FOO"]


def test_validate_application_handlers_valid():
    handlers = {"GET": {"/a": lambda: None}, "POST": {"/b": lambda: None}}
    # Should not raise
    server_utils.validate_application_handlers(handlers)


def test_validate_application_handlers_invalid_type():
    with pytest.raises(ServerValidationException):
        server_utils.validate_application_handlers(["not", "a", "dict"])


def test_validate_application_handlers_unsupported_method():
    handlers = {"GET": {"/a": lambda: None}, "FOO": {"/b": lambda: None}}
    with pytest.raises(ServerValidationException):
        server_utils.validate_application_handlers(handlers)
