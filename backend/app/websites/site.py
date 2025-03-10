from typing import Protocol

from app.schemas import TempBook, TempChapter


# 协议类
class Site(Protocol):
    def get_domain(self) -> str:
        """
        获取对应网站实例的域名

        Returns:
            str: 域名
        """
        ...

    def search(self, keyword: str) -> list[TempBook]:
        """
        对应网站的搜索 api

        Args:
            keyword (str): 搜索关键字

        Returns:
            list[TempBookInfo]: 搜索结果
        """
        ...

    def get_chapters(self, book_url: str) -> list[TempChapter]:
        """
        获取对应域名对应小说的章节信息

        Args:
            book_url (str): 需要获取章节信息的小说链接

        Returns:
            list[Chapter]: 章节信息列表
        """
        ...

    def get_content(self, chapter_url: str) -> str:
        """
        获取对应域名对应章节的内容

        Args:
            chapter_url (str): 需要获取内容的章节链接

        Returns:
            str: 章节内容
        """
        ...
