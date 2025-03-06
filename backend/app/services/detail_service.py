from sqlmodel import Session, select

from app.models import BookInfo
from app.schemas import BookDetail
from app.websites.mapping import get_site_instance


async def get_detail(id: int, session: Session) -> BookDetail | None:
    book_detail = None

    book_info = get_book_info_by_id(id, session)
    if book_info:
        book_domain = book_info.book_domain
        site_instance = get_site_instance(book_domain)
        chapter_info = await site_instance.get_chapter_info(book_info.book_url)
        book_detail = BookDetail(book_info=book_info, chapter_info_list=chapter_info)

    return book_detail


def get_book_info_by_id(id: int, session: Session) -> BookInfo | None:
    result = session.exec(select(BookInfo).where(BookInfo.book_id == id)).first()
    return result
