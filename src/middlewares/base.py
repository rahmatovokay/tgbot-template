from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from typing import Callable, Dict, Any, Awaitable

from src.locales import translator

class InitMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user = getattr(event, "from_user", getattr(event, "user", None))
        if user:
            language_code = user.language_code or "en"
        else:
            language_code = "en"

        data["_"] = await translator.get_translator(language_code)

        return await handler(event, data)

