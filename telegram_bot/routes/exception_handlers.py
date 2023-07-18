from typing import TYPE_CHECKING

from fastapi import Request, Response
from fastapi.exception_handlers import (
    http_exception_handler,
)
from starlette.exceptions import HTTPException

from ..logging import get_logger

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = get_logger()


def register_exception_handlers(app: "FastAPI"):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(
        request: Request, exc: HTTPException
    ) -> Response:
        logger.error("", exc_info=exc)
        return await http_exception_handler(request, exc)
