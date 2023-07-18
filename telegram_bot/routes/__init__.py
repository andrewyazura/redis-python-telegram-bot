from typing import TYPE_CHECKING

from .exception_handlers import register_exception_handlers
from .telegram_webhook import router as telegram_webhook_router

if TYPE_CHECKING:
    from fastapi import FastAPI


def register_routes(app: "FastAPI") -> None:
    register_exception_handlers(app)

    app.include_router(telegram_webhook_router)
