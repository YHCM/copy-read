from fastapi import FastAPI

from app.database import create_db
from app.routers import api

app = FastAPI()

# 创建数据库（如果不存在的话）
create_db()

app.include_router(api.router)
