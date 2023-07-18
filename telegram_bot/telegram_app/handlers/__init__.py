from typing import TYPE_CHECKING

from ...config import get_settings
from ...redis_store import get_store
from ..custom_conversation_handler import CustomConversationHandler
from .get_age import handler as get_age_handler
from .get_name import handler as get_name_handler
from .start import handler as start_handler
from .types import MainMenu

if TYPE_CHECKING:
    from telegram.ext import Application


def register_handlers(telegram_app: "Application") -> None:
    settings = get_settings()

    telegram_app.add_handler(
        CustomConversationHandler(
            name="main_menu",
            conversation_store=get_store(settings.redis_conversations),
            entry_points=[start_handler],
            states={
                MainMenu.NAME: [get_name_handler],
                MainMenu.AGE: [get_age_handler],
            },
            fallbacks=[start_handler],
        )
    )
