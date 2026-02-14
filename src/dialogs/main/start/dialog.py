from aiogram import types
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Row, Url, Button
from aiogram_dialog.api.entities.launch_mode import LaunchMode

from src.utils.files import Banner
from src.locales.translator import AioDialogTranslate as _

from .other import *
from . import states

start = Dialog(
    Window(
        _("start-msg"),
        StaticMedia(
            url=Banner("night.jpg"),
            type=types.ContentType.PHOTO,
        ),
        getter=get_data,
        state=states.Start.default,
    ),
    launch_mode=LaunchMode.ROOT
)
