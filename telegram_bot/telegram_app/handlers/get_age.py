from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .types import MainMenu


async def callback(update: Update, context: CallbackContext) -> str:
    text = update.effective_message.text

    try:
        context.user_data["age"] = int(text)
    except ValueError:
        await update.effective_message.reply_text(
            "That's not a number", quote=True
        )
        return MainMenu.AGE

    await update.effective_message.reply_text("Good!", quote=True)
    return ConversationHandler.END


handler = MessageHandler(filters.TEXT & (~filters.COMMAND), callback)
