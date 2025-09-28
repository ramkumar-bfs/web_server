# 3rd Party Imports
import os
import uvicorn

# Local imports
from . import constants as CONSTANTS

if __name__ == "__main__":
    # TODO: Replace environment module to get env
    uvicorn.run(
        "web_server.main:app",
        host=os.environ[CONSTANTS.WEB_SERVER_HOST],
        port=int(os.environ[CONSTANTS.WEB_SERVER_PORT]),
        reload=True,
    )
