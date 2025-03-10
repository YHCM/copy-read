from fastapi import FastAPI

from app.database import create_database
from app.routers import authors, books, root

app = FastAPI()

# 创建数据库（如果不存在的话）
create_database()

# 设置路由
app.include_router(root.router)
app.include_router(authors.router)
app.include_router(books.router)
