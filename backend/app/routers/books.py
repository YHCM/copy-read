from fastapi import APIRouter
from starlette import status

from app.database import SessionDep
from app.schemas import BookInfo, Result
from app.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=Result)
def books(session: SessionDep):
    books = book_service.get_all_books(session)
    result = Result(code=status.HTTP_200_OK, message="所有书籍信息", data=books)

    return result


@router.get("/{book_id}", response_model=Result)
def get_book(session: SessionDep, book_id: int):
    book = book_service.get_book_by_id(session, book_id)
    if book:
        result = Result(code=status.HTTP_200_OK, message="书籍信息", data=book)
    else:
        result = Result(code=status.HTTP_404_NOT_FOUND, message="书籍不存在", data=None)

    return result


@router.get("/{book_id}/chapters", response_model=Result)
def get_chapters(session: SessionDep, book_id: int):
    book = book_service.get_book_by_id(session, book_id)
    if book:
        book_service.parse_book(session, book.book_id)

        book_data = BookInfo.model_validate(book)
        result = Result(code=status.HTTP_200_OK, message="书籍信息", data=book_data)
    else:
        result = Result(code=status.HTTP_404_NOT_FOUND, message="作者不存在", data=None)

    return result


@router.get("/{book_id}/chapters/{chapter_id}", response_model=Result)
def get_content(session: SessionDep, book_id: int, chapter_id: int):
    content = book_service.get_content(session, book_id, chapter_id)

    result = Result(code=status.HTTP_200_OK, message="章节信息", data=content)

    return result
