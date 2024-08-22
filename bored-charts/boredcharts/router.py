from collections.abc import Callable

from fastapi import APIRouter
from fastapi.types import DecoratedCallable


class BCRouter(APIRouter):
    def chart(
        self,
        name: str,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        path = f"/figure/{name}"
        return self.api_route(
            path=path,
            name=name,
        )
