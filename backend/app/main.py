from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth as auth_router
from .routers import db_health as db_health_router
from .routers import health as health_router
from .routers import items as items_router
from .version import APP_NAME, APP_VERSION


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION)

    # CORS (allow FE origin and cookies)
    allow_origins: list[str] = []
    if settings.cors_origins:
        allow_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    # sensible defaults for local dev if not explicitly configured
    if not allow_origins and settings.environment == "local":
        allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health_router.router)
    app.include_router(db_health_router.router)
    app.include_router(auth_router.router)
    app.include_router(items_router.router)

    return app


app = create_app()
