from sqlmodel import Session

from app.models import Book
from app.services import book_service
from app.websites.mapping import get_site_instances


def search(session: Session, keyword: str, mode: str) -> list[Book]:
    """
    搜索 api

    Args:
        mode (str): 搜索模式
        keyword (str): 搜索关键字

    Returns:
        list[Book]: 搜索结果
    """
    search_modes = {
        "local": lambda: local_search(session, keyword),
        "network": lambda: network_search(session, keyword),
        "default": lambda: local_search(session, keyword)
        or network_search(session, keyword),
    }

    results = search_modes.get(mode, lambda: [])()

    return results


def local_search(session: Session, keyword: str) -> list[Book]:
    books = book_service.search_book(session, keyword)
    return books


def network_search(session: Session, keyword: str) -> list[Book]:
    temp_results = []

    # 获取网站实例
    site_instances = get_site_instances()

    for site in site_instances:
        sub_results = site.search(keyword)
        temp_results.extend(sub_results)

    # 将搜索结果写入数据库
    book_service.add_books(session, temp_results)

    # 获取本地搜索的结果
    finall_results = book_service.search_book(session, keyword)

    return finall_results
