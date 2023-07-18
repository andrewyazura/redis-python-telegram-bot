from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_webhook_token: str

    redis_host: str
    redis_port: int

    redis_context_data: int
    redis_conversations: int

    logger_name: str
    logger_level: str
    logger_date_format: str

    logger_format_default: str
    logger_format_uvicorn: str
    logger_format_uvicorn_access: str

    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()  # type: ignore [call-arg]
