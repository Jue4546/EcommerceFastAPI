import subprocess

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.v1 import test_route, user_route, auth_route, goods_route

load_dotenv()

app = FastAPI()

# 添加路由
app.include_router(user_route.router)  # 添加用户管理模块的路由
app.include_router(auth_route.router)  # 添加认证模块的路由
app.include_router(test_route.router)  # 添加测试模块的路由，用于判断服务是否正常运行
app.include_router(goods_route.router) # 添加商品管理模块的路由

@app.get("/")
async def read_root():
    html_file_path = "assets/index.html"
    return FileResponse(html_file_path)


@app.on_event("startup")
async def startup_event():
    """初始化：数据库"""
    try:
        print("Start to initialize database...")
        alembic_command = "alembic upgrade head"
        subprocess.run(alembic_command, shell=True, check=True)
        print("Database initialization completed!")
    except subprocess.CalledProcessError as e:
        print(f"Error while initializing database: {e}")
    # 仅在开发环境下使用
    # if os.getenv('API_URL') == 'http://localhost:8000' and not account.is_authenticated: account.authenticate()
