from fastapi import APIRouter
from starlette import status

from app.database import SessionDep
from app.schemas import Result
from app.services import search_service

router = APIRouter(prefix="", tags=["root"])


@router.get("/", response_model=Result)
def root():
    return Result(code=status.HTTP_200_OK, message="success", data="root")


@router.get("/search", response_model=Result)
def search(session: SessionDep, keyword: str, mode: str = "default"):
    """
    **参数**
    - keyword (str): 搜索关键字
    - mode (str): 搜索模式
        - local: 仅本地搜索
        - network: 仅网络搜索
        - default: 默认，先进行本地搜索，如果有结果，返回，没有结果在进行网络搜索
    """
    books = search_service.search(session, keyword, mode)
    result = Result(
        code=status.HTTP_200_OK, message=f"搜索书籍，关键字：{keyword}", data=books
    )

    return result
