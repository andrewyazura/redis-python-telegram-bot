from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .logging import configure_logging
from .routes import register_routes
from .telegram_app import get_telegram_app
from .telegram_app.handlers import register_handlers


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator[None, None]:
    telegram_app = get_telegram_app()

    register_handlers(telegram_app)

    await telegram_app.initialize()
    yield
    await telegram_app.shutdown()


def build_app() -> FastAPI:
    configure_logging()

    app = FastAPI(lifespan=lifespan)
    register_routes(app)

    return app
