from typing import Annotated, Optional

from fastapi import APIRouter, Header, HTTPException, Response, status
from pydantic import BaseModel
from telegram import Update

from ..config import get_settings
from ..telegram_app import get_telegram_app


class TelegramWebhook(BaseModel):
    update_id: int

    message: Optional[dict] = None
    edited_message: Optional[dict] = None

    channel_post: Optional[dict] = None
    edit_channel_post: Optional[dict] = None

    inline_query: Optional[dict] = None
    chosen_inline_result: Optional[dict] = None
    callback_query: Optional[dict] = None
    shipping_query: Optional[dict] = None
    pre_checkout_query: Optional[dict] = None

    poll: Optional[dict] = None
    poll_answer: Optional[dict] = None

    my_chat_member: Optional[dict] = None
    chat_member: Optional[dict] = None
    chat_join_request: Optional[dict] = None


router = APIRouter(tags=["telegram"])


@router.post("/")
async def handle_telegram_webhook(
    telegram_webhook: TelegramWebhook,
    x_telegram_bot_api_secret_token: Annotated[Optional[str], Header()] = None,
) -> Response:
    if (
        x_telegram_bot_api_secret_token
        != get_settings().telegram_webhook_token
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    telegram_app = get_telegram_app()

    update = Update.de_json(dict(telegram_webhook), telegram_app.bot)
    await telegram_app.process_update(update)

    return Response(status_code=status.HTTP_200_OK)
