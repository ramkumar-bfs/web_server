from web_server.utils import application_utils


def test_handle_exception():
    status, content_type, content = application_utils.handle_exception(
        500, "SomeError", "Something went wrong"
    )
    assert status == 500
    assert content_type == "application/json"
    assert content["error_code"] == 500
    assert content["error_type"] == "SomeError"
    assert content["error_msg"] == "Something went wrong"
