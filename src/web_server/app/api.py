# 3rd party imports
from fastapi import APIRouter, Body, BackgroundTasks

# Local Imports
from .models import RenderRequest
from ..utils import run_echo_new_window

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello Modular FastAPI"}


@router.post("/submit_nuke_copycat_render")
async def submit_nuke_copycat_render(
    render_req: RenderRequest = Body(...),
    background_tasks: BackgroundTasks = None,
):
    background_tasks.add_task(run_echo_new_window, render_req.message)
    return {"detail": "Echo command scheduled in new window"}
