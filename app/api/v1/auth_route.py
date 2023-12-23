"""认证路由：api/auth_route.py"""
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.utils.email_utils import account, scopes
from dotenv import load_dotenv
load_dotenv()
callback = os.getenv('API_URL') + "/auth/microsoft/callback"

router = APIRouter()


class MyDB:
    state = None


my_db = MyDB()


@router.get("/auth/microsoft")
async def auth_step_one():
    url, state = account.con.get_authorization_url(requested_scopes=scopes, redirect_uri=callback)
    my_db.state = state  # 存储状态
    return RedirectResponse(url)


@router.get("/auth/microsoft/callback")
async def auth_step_two_callback(code: str):
    my_saved_state = my_db.state  # 获取存储的状态
    result = account.con.request_token(code, state=my_saved_state, redirect_uri=callback)
    if result:
        return {"message": "Authentication successful. Token stored."}
    else:
        raise HTTPException(status_code=400, detail="Authentication failed.")
