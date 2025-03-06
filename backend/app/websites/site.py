from typing import Protocol

from app.models import BookInfo


# 接口类
class Site(Protocol):
    def get_domain(self) -> str:
        """
        获取对应网站实例的域名

        Returns:
            str: 域名
        """
        ...

    async def search(self, keyword: str) -> list[BookInfo]:
        """
        www.kunnu.com 的搜索 api

        Args:
            keyword (str): 搜索关键字

        Returns:
            list[BookInfo]: 搜索结果
        """
        ...
