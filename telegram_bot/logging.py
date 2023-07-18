from functools import cache
from logging import getLogger
from logging.config import dictConfig
from typing import TYPE_CHECKING

from .config import get_settings

if TYPE_CHECKING:
    from logging import Logger


def configure_logging() -> None:
    settings = get_settings()
    logger_level = settings.logger_level

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": settings.logger_format_default,
                    "datefmt": settings.logger_date_format,
                },
                "uvicorn": {
                    "format": settings.logger_format_uvicorn,
                    "datefmt": settings.logger_date_format,
                },
                "uvicorn_access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "format": settings.logger_format_uvicorn_access,
                    "datefmt": settings.logger_date_format,
                },
            },
            "handlers": {
                "stdout": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "uvicorn": {
                    "formatter": "uvicorn",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "uvicorn_access": {
                    "formatter": "uvicorn_access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                settings.logger_name: {
                    "handlers": ["stdout"],
                    "level": logger_level,
                },
                "uvicorn": {
                    "handlers": ["uvicorn"],
                    "level": logger_level,
                },
                "uvicorn.access": {
                    "handlers": ["uvicorn_access"],
                    "level": logger_level,
                },
            },
        }
    )


@cache
def get_logger() -> "Logger":
    return getLogger(get_settings().logger_name)
