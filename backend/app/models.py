# 这个文件是存放数据库表的模型
from sqlmodel import Field, SQLModel


# 存储搜索的结果，方便之后搜索
class BookInfo(SQLModel, table=True):
    __tablename__ = "book_info"  # type: ignore

    # SQLite 中，主键是整数类型，默认为自动递增
    book_id: int = Field(default=None, primary_key=True)
    book_domain: str
    book_url: str
    book_name: str
