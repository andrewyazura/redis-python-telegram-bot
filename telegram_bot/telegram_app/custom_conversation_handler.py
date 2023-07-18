from collections.abc import MutableMapping

from telegram import Update
from telegram.ext._conversationhandler import ConversationHandler

from ..redis_store import PrefixedMapping as PM


class CustomConversationHandler(ConversationHandler):
    def __init__(
        self, conversation_store: MutableMapping, name: str, *args, **kwargs
    ) -> None:
        super().__init__(name=name, *args, **kwargs)

        self._conversations = PM(conversation_store, (name,))

    def _get_key(self, update: Update) -> str:
        return ":".join(str(i) for i in super()._get_key(update))
