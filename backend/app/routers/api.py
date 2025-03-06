from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models import BookInfo
from app.schemas import BookDetail
from app.services import detail_service, search_service

router = APIRouter(prefix="/api", tags=["api"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/search", response_model=list[BookInfo])
async def search(session: SessionDep, keyword: str, mode: str = "default"):
    return await search_service.search(keyword, mode, session)


@router.get("/detail", response_model=BookDetail)
async def get_detail(session: SessionDep, book_id: int):
    return await detail_service.get_detail(book_id, session)
