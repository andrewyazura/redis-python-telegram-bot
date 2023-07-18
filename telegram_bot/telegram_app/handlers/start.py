from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from .types import MainMenu


async def callback(update: Update, context: CallbackContext) -> str:
    await update.effective_message.reply_text("Hey! Give me your name")

    return MainMenu.NAME


handler = CommandHandler("start", callback)
