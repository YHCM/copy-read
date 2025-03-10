# 数据库模型
from sqlmodel import Field, Relationship, SQLModel


# 作者信息表
class Author(SQLModel, table=True):
    __tablename__ = "author"  # type: ignore

    author_id: int = Field(default=None, primary_key=True)
    author_name: str

    # 通过 Relationship 进行 一对多 关联
    books: list["Book"] | None = Relationship(back_populates="author")


# 小说信息表
class Book(SQLModel, table=True):
    __tablename__ = "book"  # type: ignore

    book_id: int = Field(default=None, primary_key=True)
    book_title: str
    book_url: str
    book_domain: str
    author_id: int = Field(
        foreign_key="author.author_id"  # 外键关联到 author 表
    )

    # 通过 Relationship 进行 一对多 关联
    author: Author | None = Relationship(back_populates="books")
    chapters: list["Chapter"] | None = Relationship(back_populates="book")


# 章节信息表
class Chapter(SQLModel, table=True):
    __tablename__ = "chapter"  # type: ignore

    book_id: int = Field(foreign_key="book.book_id", primary_key=True)
    chapter_id: int = Field(default=None, primary_key=True)
    chapter_title: str
    chapter_url: str

    # 通过 Relationship 进行 一对多 关联
    book: Book | None = Relationship(back_populates="chapters")
