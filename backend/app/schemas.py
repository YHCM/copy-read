# 这个文件是存放请求和响应的模型
from pydantic import BaseModel

from app.models import BookInfo


class ChapterInfo(BaseModel):
    chapter_id: int
    chapter_url: str
    chapter_title: str


class BookDetail(BaseModel):
    book_info: BookInfo
    chapter_info_list: list[ChapterInfo]
