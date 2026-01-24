import inspect

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

class Func(Text):
    def __init__(
        self,
        func,
        when: WhenCondition = None,
        **kwargs
    ):
        super().__init__(when=when)
        self.func = func
        self.kwargs = kwargs

    async def _render_text(
        self,
        data: dict,
        manager: DialogManager
    ) -> str:
        if callable(self.func):
            result = self.func(**self.kwargs)
            if inspect.iscoroutine(result):
                return await result
            return str(result)
        
        return str(self.func)
