from typing import Protocol

from app.models import BookInfo
from app.schemas import ChapterInfo


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
        对应域名的搜索 api

        Args:
            keyword (str): 搜索关键字

        Returns:
            list[BookInfo]: 搜索结果
        """
        ...

    async def get_chapter_info(self, book_url: str) -> list[ChapterInfo]:
        """
        对应域名获取对应小说的章节信息

        Args:
            book_url (str): 需要获取信息的小说链接

        Returns:
            list[ChapterInfo]: 获取的结果
        """
        ...
