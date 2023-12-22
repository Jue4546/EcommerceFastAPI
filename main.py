from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.v1 import test_route, user_route
from db.base import *

app = FastAPI()

# 添加路由
app.include_router(user_route.router)  # 添加用户管理模块的路由
app.include_router(test_route.router)  # 添加测试模块的路由，用于判断服务是否正常运行


@app.get("/")
async def read_root():
    html_file_path = "assets/index.html"
    return FileResponse(html_file_path)


@app.on_event("startup")
async def startup_event():
    """初始化"""
    if not tables_exist():
        create_tables_if_not_exist()
    if not admin_exist():
        create_admin_if_not_exists()
