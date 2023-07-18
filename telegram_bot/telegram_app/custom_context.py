from telegram.ext import CallbackContext, ExtBot

from ..config import get_settings
from ..redis_store import PrefixedMapping as PM
from ..redis_store import get_store

context_data = get_store(get_settings().redis_context_data)


class CustomContext(CallbackContext[ExtBot, PM, PM, PM]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_data_mediator = PM(context_data, ("user", self._user_id))
        self.chat_data_mediator = PM(context_data, ("chat", self._chat_id))
        self.bot_data_mediator = PM(context_data, ("bot",))

    @property
    def user_data(self) -> PM:
        return self.user_data_mediator

    @property
    def chat_data(self) -> PM:
        return self.chat_data_mediator

    @property
    def bot_data(self) -> PM:
        return self.bot_data_mediator
