from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False 可以让 FastAPI 在不同线程使用同一个 SQLite 数据库
# 因为单个请求可能会使用多个线程
# 最好确保每个请求使用一个单独的 SQLModel 会话(Session)
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db() -> None:
    """创建数据库（如果不存在）"""
    SQLModel.metadata.create_all(engine)


# Session 表示生成器会返回 Session 类型对象
# None 表示生成器没有返回值（即不会有 send 操作）
# None 表示生成器没有异常处理类型（即没有 throw 操作）
def get_session() -> Generator[Session, None, None]:
    """返回一个 SQLModel 会话，用来操作数据库"""
    with Session(engine) as session:
        yield session
