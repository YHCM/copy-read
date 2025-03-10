# http 请求响应模型
from typing import Any

from pydantic import BaseModel


# 统一响应模型
class Result(BaseModel):
    code: int
    message: str
    data: Any


# 临时书籍信息存储（因为爬取类不可以操作数据库，无法知道作者 id）
class TempBook(BaseModel):
    book_title: str
    book_url: str
    book_domain: str
    author_name: str


# 临时章节信息存储
class TempChapter(BaseModel):
    book_url: str
    chapter_id: int
    chapter_title: str
    chapter_url: str


# 作者信息基类
class AuthorBase(BaseModel):
    author_id: int
    author_name: str

    class Config:
        from_attributes = True


# 书籍信息基类
class BookBase(BaseModel):
    book_id: int
    book_title: str

    class Config:
        from_attributes = True


# 章节信息基类
class ChapterBase(BaseModel):
    chapter_id: int
    chapter_title: str

    class Config:
        from_attributes = True


# 作者信息，带所有作品
class AuthorInfo(AuthorBase):
    books: list[BookBase] | None  # 所有作品


# 书籍信息，带所有章节
class BookInfo(BookBase):
    chapters: list[ChapterBase] | None
