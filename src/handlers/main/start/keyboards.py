from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

async def start_keyboard(_) -> ReplyKeyboardMarkup:

    keyboard = ReplyKeyboardBuilder()
    
    # keyboard.add(
    #     types.KeyboardButton(text=f"💎‎⁢ {await _("menu-keyboard")}")
    # )

    return keyboard.as_markup(resize_keyboard=True)