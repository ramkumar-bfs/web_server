# 3rd party imports
from fastapi import FastAPI

# Local imports
from .api import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
