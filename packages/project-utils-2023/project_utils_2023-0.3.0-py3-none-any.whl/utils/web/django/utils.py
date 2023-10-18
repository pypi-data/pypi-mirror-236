from typing import Callable, Any
from asgiref.sync import sync_to_async


class DjangoUtils:
    @staticmethod
    async def to_async_fun(fun: Callable, *args, **kwargs) -> Any:
        return await sync_to_async(fun)(*args, **kwargs)
