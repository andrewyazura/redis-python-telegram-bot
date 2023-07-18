from functools import cache

from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, Defaults

from ..config import get_settings
from .custom_context import CustomContext


@cache
def get_telegram_app() -> Application:
    context_types = ContextTypes(context=CustomContext)
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN)

    telegram_app = (
        Application.builder()
        .token(get_settings().telegram_bot_token)
        .concurrent_updates(True)
        .context_types(context_types)
        .defaults(defaults)
        .build()
    )

    return telegram_app
