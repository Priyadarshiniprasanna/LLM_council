"""
Arinar FastAPI application entry point.

Mounts all v1 routers and configures middleware, CORS, and lifecycle hooks.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import debate_routes, document_routes, identity_routes, persona_routes
from app.config import settings
from app.db.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and tear down resources around the app lifecycle."""
    await init_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    if settings.sentry_dsn:
        sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.app_env)

    application = FastAPI(
        title="Arinar API",
        version="0.1.0",
        description="LLM Council backend — debate orchestration, personas, and document services.",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.app_debug else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _mount_routers(application)
    return application


def _mount_routers(app: FastAPI) -> None:
    prefix = "/api/v1"
    app.include_router(debate_routes.router, prefix=prefix, tags=["debates"])
    app.include_router(persona_routes.router, prefix=prefix, tags=["personas"])
    app.include_router(document_routes.router, prefix=prefix, tags=["documents"])
    app.include_router(identity_routes.router, prefix=prefix, tags=["identity"])


app = create_app()
