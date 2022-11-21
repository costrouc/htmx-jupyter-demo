import pathlib

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import htmx_jupyter
from htmx_jupyter import views


def create_app():
    app = FastAPI()

    module_directory = pathlib.Path(htmx_jupyter.__file__).parent
    templates = Jinja2Templates(directory=module_directory / "templates")
    fragments = Jinja2Templates(directory=module_directory / "fragments")

    @app.middleware("http")
    async def conda_store_middleware(request: Request, call_next):
        request.state.templates = templates
        request.state.fragments = fragments
        response = await call_next(request)
        return response

    app.mount("/static", StaticFiles(directory=module_directory / "static"), name="static")
    app.include_router(views.router_ui)

    return app

app = create_app()
