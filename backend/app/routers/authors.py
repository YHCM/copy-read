from fastapi import APIRouter
from starlette import status

from app.database import SessionDep
from app.schemas import AuthorInfo, Result
from app.services import author_service

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("", response_model=Result)
def authors(session: SessionDep):
    authors = author_service.get_all_authors(session)
    result = Result(code=status.HTTP_200_OK, message="所有作者信息", data=authors)

    return result


@router.get("/{author_id}", response_model=Result)
def get_author(session: SessionDep, author_id: int):
    author = author_service.get_author_by_id(session, author_id)
    if author:
        author_data = AuthorInfo.model_validate(author)
        result = Result(code=status.HTTP_200_OK, message="作者信息", data=author_data)
    else:
        result = Result(code=status.HTTP_404_NOT_FOUND, message="作者不存在", data=None)

    return result
