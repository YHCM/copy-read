from sqlmodel import Session, select

from app.models import Author


def add_author(session: Session, author_name: str) -> Author:
    """
    传入 author_name，往 author 表中添加数据

    Args:
        session (Session): SQLModel 会话
        author_name (str): 作者名字

    Returns:
        Author: 返回添加的作者信息
    """

    # 先查看是否存在
    if is_author_existed(session, author_name):
        author = get_author_by_name(session, author_name)
    else:
        author = Author(author_name=author_name)
        session.add(author)
        session.commit()

    # 确保 author 不是 None
    assert author is not None, "Author should not be None"
    return author


def get_all_authors(session: Session) -> list[Author]:
    """
    获取所有的作者信息

    Args:
        session (Session): SQLModel 会话

    Returns:
        list[Author]: 返回所有的作者信息
    """
    statement = select(Author)
    authors = session.exec(statement).all()
    return list(authors)


def get_author_by_name(session: Session, author_name: str) -> Author | None:
    """
    通过作者名字获取作者信息

    Args:
        session (Session): SQLModel 会话
        author_name (str): 作者名字

    Returns:
        Author | None: 返回搜索到的作者信息，或者 None
    """
    statement = select(Author).where(Author.author_name == author_name)
    author = session.exec(statement).first()

    return author


def get_author_by_id(session: Session, author_id: int) -> Author | None:
    """
    通过作者 id 获取作者信息

    Args:
        session (Session): SQLModel 会话
        author_id (int): 作者 id

    Returns:
        Author | None: 返回搜索到的作者信息，或者 None
    """
    # statement = select(Author).where(Author.author_id == author_id)
    # author = session.exec(statement).first()
    author = session.get(Author, author_id)
    return author


def search_author(session: Session, keyword: str) -> list[Author]:
    """
    通过关键词模糊搜索

    Args:
        session (Session): SQLModel 会话
        keyword (str): 关键词

    Returns:
        list[Author]: 返回搜索到所有符合的作者信息
    """
    statement = select(Author).where(Author.author_name.ilike(f"%{keyword}%"))  # type: ignore
    authors = session.exec(statement).all()
    return list(authors)


def is_author_existed(session: Session, author_name: str) -> bool:
    statement = select(Author).where(Author.author_name == author_name)
    author = session.exec(statement).first()

    return author is not None


if __name__ == "__main__":
    from sqlmodel import Session

    from app.database import create_database, engine

    create_database()

    with Session(engine) as session:
        authors = get_all_authors(session)

        for author in authors:
            print(author.model_dump_json)
            print(author.books)
