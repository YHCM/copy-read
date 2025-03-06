from typing import Protocol

from app.models import BookInfo


# 接口类
class Site(Protocol):
    def get_domain(self) -> str: ...

    async def search(self, keyword: str) -> list[BookInfo]: ...
