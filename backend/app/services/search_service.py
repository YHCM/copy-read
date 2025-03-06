from sqlmodel import Session, select

from app.models import BookInfo
from app.websites.mapping import get_site_instance
from app.websites.site import Site


async def get_site_instances() -> list[Site]:
    # 启用的域名
    enable_domain = ["www.kunnu.com", "www.sudugu.com"]
    return [get_site_instance(domain=domain) for domain in enable_domain]


async def search(keyword: str, mode: str, session: Session) -> list[BookInfo]:
    """
    搜索方法

    Args:
        keyword (str): 搜索关键字
        mode (str): 搜索模式选择

    Retruns:
        list[BookInfo]: 搜索结果
    """
    match mode:
        case "local":
            results = local_search(keyword, session)
        case "network":
            results = await network_search(keyword, session)
        case "default":
            results = local_search(keyword, session)
            if not results:
                # 如果在本地没有搜索到，进行网络搜索
                results = await network_search(keyword, session)
        case _:
            results = []

    # lambda 不可以调用异步函数，不可以使用 await
    # search_modes = {
    #     "local": lambda: local_search(keyword, session),
    #     "network": lambda: await network_search(keyword, session),
    #     "default": lambda: local_search(keyword, session)
    #     or await network_search(keyword, session),
    # }

    # results = search_modes.get(mode, lambda: [])()

    return results


def local_search(keyword: str, session: Session) -> list[BookInfo]:
    return search_book_info(keyword, session)


async def network_search(keyword: str, session: Session) -> list[BookInfo]:
    results = []

    # 获取对应网站的实例
    site_instances = await get_site_instances()

    for site_instance in site_instances:
        sub_results = await site_instance.search(keyword=keyword)
        results.extend(sub_results)

    # 将搜索结果添加进数据库
    add_book_info_list(results, session)

    finall_results = search_book_info(keyword, session)

    return finall_results


def search_book_info(keyword: str, session: Session) -> list[BookInfo]:
    results = session.exec(
        select(BookInfo).where(BookInfo.book_name.ilike(f"%{keyword}%"))  # type: ignore
    ).all()
    return list(results)


def is_book_url_existed(url: str, session: Session) -> bool:
    return (
        session.exec(select(BookInfo).where(BookInfo.book_url == url)).first()
        is not None
    )


def add_book_info_list(book_info_list: list[BookInfo], session: Session) -> None:
    for book_info in book_info_list:
        if not is_book_url_existed(book_info.book_url, session):
            add_book_info(book_info, session)


def add_book_info(book_info: BookInfo, session: Session) -> None:
    session.add(book_info)
    session.commit()
    session.refresh(book_info)


if __name__ == "__main__":
    import asyncio

    from sqlmodel import Session

    from app.database import engine

    with Session(engine) as session:
        book_info_list = asyncio.run(network_search("斗罗", session))
        print(book_info_list)
