import hashlib
from typing import Any

from aiogram.types import Message

from src import config, get_redis_client

from . import i18n
from .ai import (
    TRANSLATION_FAILURE_TTL,
    TRANSLATION_SUCCESS_TTL,
    ai_translator,
)


LANGUAGE_ALIASES = {
    "ua": "uk",
}


def normalize_language_code(language_code: str | None) -> str:
    normalized = (language_code or config.DEFAULT_LANGUAGE).strip().lower().replace("_", "-")
    if not normalized:
        return config.DEFAULT_LANGUAGE.lower()

    if normalized in LANGUAGE_ALIASES:
        return LANGUAGE_ALIASES[normalized]

    if "-" not in normalized:
        return normalized

    return normalized.split("-", 1)[0]


def get_message_language_code(message: Message | None) -> str:
    if message is None:
        return config.DEFAULT_LANGUAGE

    from_user = getattr(message, "from_user", None)
    user_language = getattr(from_user, "language_code", None)
    if isinstance(user_language, str) and user_language.strip():
        return user_language

    return config.DEFAULT_LANGUAGE


async def make_cache_key(template_text: str, target: str) -> str:
    text_hash = hashlib.md5(template_text.encode("utf-8")).hexdigest()
    return f"handler_translation:{target}:{text_hash}"


async def _(key: str, message: Message | None = None, **params: Any) -> str:
    template_text = i18n.format_value(key)

    if template_text == key:
        return key.format(**params) if params else key

    language_code = normalize_language_code(get_message_language_code(message))
    default_language = normalize_language_code(config.DEFAULT_LANGUAGE)

    if language_code == default_language:
        translated_template = template_text
    else:
        cache_key = await make_cache_key(template_text, language_code)
        redis_client = await get_redis_client()
        cached_translation = await redis_client.get(cache_key)

        if cached_translation:
            translated_template = cached_translation
        else:
            translated_template = await ai_translator.translate(template_text, language_code)
            cache_ttl = TRANSLATION_SUCCESS_TTL

            if translated_template is None:
                translated_template = template_text
                cache_ttl = TRANSLATION_FAILURE_TTL

            await redis_client.set(cache_key, translated_template, ex=cache_ttl)

    return translated_template.format(**params) if params else translated_template
