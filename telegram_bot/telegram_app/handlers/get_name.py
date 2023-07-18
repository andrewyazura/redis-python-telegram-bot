from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from .types import MainMenu


async def callback(update: Update, context: CallbackContext) -> str:
    context.user_data["name"] = update.effective_message.text

    await update.effective_message.reply_text(
        "Nice name! Now give me your age", quote=True
    )
    return MainMenu.AGE


handler = MessageHandler(filters.TEXT & (~filters.COMMAND), callback)
