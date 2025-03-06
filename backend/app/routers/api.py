from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models import BookInfo
from app.services import search_service

router = APIRouter(prefix="/api", tags=["api"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/search")
async def search(
    session: SessionDep, keyword: str, mode: str = "default"
) -> list[BookInfo]:
    return await search_service.search(keyword, mode, session)
