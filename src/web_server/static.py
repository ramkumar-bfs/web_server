import os

# TODO: Never ever do this, use a proper web framework
# NOTE: This is just for demonstration purposes
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")


def get_static_file(filename):
    file_path = os.path.join(STATIC_ROOT, filename)
    if not os.path.isfile(file_path):
        return None, None, None
    if filename.endswith(".html"):
        content_type = "text/html"
    elif filename.endswith(".css"):
        content_type = "text/css"
    elif filename.endswith(".js"):
        content_type = "application/javascript"
    elif filename.endswith(".png"):
        content_type = "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        content_type = "image/jpeg"
    else:
        content_type = "application/octet-stream"
    with open(file_path, "rb") as f:
        content = f.read()
    return 200, content_type, content
