from sqlmodel import Session, select

from app.models import Book, Chapter
from app.schemas import TempBook, TempChapter
from app.services import author_service
from app.websites.mapping import get_site_instance


def add_book(session: Session, temp_book: TempBook) -> Book:
    author_name = temp_book.author_name
    author = author_service.get_author_by_name(session, author_name)

    # 如果 author 在表中
    if author:
        author_id = author.author_id
    else:  # 如果不在表中，先添加，在获取
        author = author_service.add_author(session, author_name)
        author_id = author.author_id

    book = Book(
        book_title=temp_book.book_title,
        book_url=temp_book.book_url,
        book_domain=temp_book.book_domain,
        author_id=author_id,
    )
    session.add(book)
    session.commit()

    return book


def add_books(session, books: list[TempBook]) -> None:
    for book in books:
        if not is_book_url_existed(session, book.book_url):  # 如果书籍不存在，添加
            add_book(session, book)


def search_book(session: Session, keyword: str) -> list[Book]:
    statement = select(Book).where(Book.book_title.ilike(f"%{keyword}%"))  # type: ignore
    books = session.exec(statement).all()

    return list(books)


def is_book_url_existed(session: Session, url: str) -> bool:
    book = get_book_by_url(session, url)

    return book is not None


def get_all_books(session: Session) -> list[Book]:
    statement = select(Book)
    books = session.exec(statement)
    return list(books)


def get_book_by_id(session: Session, book_id: int) -> Book | None:
    # statement = select(Book).where(Book.book_id == book_id)
    # book = session.exec(statement).first()
    book = session.get(Book, book_id)
    return book


def get_book_by_url(session: Session, url: str) -> Book | None:
    statement = select(Book).where(Book.book_url == url)
    book = session.exec(statement).first()

    return book


def add_chapter(session: Session, temp_chapter: TempChapter) -> Chapter:
    book = get_book_by_url(session, temp_chapter.book_url)

    if book:
        book_id = book.book_id

        chapter = Chapter(
            book_id=book_id,
            chapter_id=temp_chapter.chapter_id,
            chapter_title=temp_chapter.chapter_title,
            chapter_url=temp_chapter.chapter_url,
        )
        session.add(chapter)
        session.commit()

        return chapter
    else:
        # 异常处理，之后做
        raise


def add_chapters(session: Session, chapters: list[TempChapter]) -> None:
    for chapter in chapters:
        if not is_chapter_url_existed(session, chapter.chapter_url):
            add_chapter(session, chapter)


def is_chapter_url_existed(session: Session, url: str) -> bool:
    statement = select(Chapter).where(Chapter.chapter_url == url)
    chapter = session.exec(statement).first()

    return chapter is not None


def parse_book(session: Session, book_id: int) -> None:
    book = get_book_by_id(session, book_id)

    if book:
        site = get_site_instance(book.book_domain)
        temp_chapters = site.get_chapters(book.book_url)
        add_chapters(session, temp_chapters)


def get_content(session: Session, book_id: int, chapter_id: int) -> str:
    book = get_book_by_id(session, book_id)

    if not book or not book.chapters:
        return ""

    chapter_url = book.chapters[chapter_id - 1].chapter_url
    site = get_site_instance(book.book_domain)

    return site.get_content(chapter_url)
