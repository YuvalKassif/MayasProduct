from fastapi import FastAPI
from .config import settings
from .routers import health as health_router
from .version import APP_NAME, APP_VERSION


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    # Routers
    app.include_router(health_router.router)

    return app


app = create_app()

