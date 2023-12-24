"""用户路由：api/user_route.py"""
from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token_model import *
from app.models.user_model import *
from app.services import user_service, auth_service
from app.utils import email_utils
router = APIRouter()


@router.post("/auth", tags=["用户管理模块"], response_model=Token)
async def auth_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户认证路由"""
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if isinstance(user, str):
        error_message = user
        if error_message == "User not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        elif error_message == "Incorrect password":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"}
            )
    else:
        access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/send-verification-code", tags=["用户管理模块"])
async def send_verification_code(email: str):
    """发送验证码路由"""
    verification_code = auth_service.generate_verification_code()

    success = email_utils.send_verification_email(email, verification_code)
    if success:
        auth_service.save_verification_code(email, verification_code)
        return {"message": "Verification code sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send verification code, please try again later")


@router.post("/register", tags=["用户管理模块"])
async def register_user(username: str, password: str, email: str, verification_code: str):
    """用户注册路由"""
    user = RegisterUser(
        username=username,
        password=password,
        email=email,
        verification_code=verification_code
    )
    try:
        new_user = user_service.register_new_user(user)
        if new_user is None:
            raise HTTPException(status_code=404, detail="Failed to register user")
        if new_user.is_admin:
            return {
                "username": new_user.username,
                "message": "Admin user registered successfully."
            }
        else:
            return {
                "username": new_user.username,
                "message": "User registered successfully."
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/me", tags=["用户管理模块"], response_model=BaseUser)
async def get_user_info(current_user: BaseUser = Depends(auth_service.get_current_active_user)):
    """用户信息获取路由"""
    return current_user


@router.get("/user/all", tags=["用户管理模块"], response_model=List[BaseUser])
async def get_all_users_info(current_user: BaseUser = Depends(auth_service.get_current_active_user)):
    """用户信息获取路由"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    all_users = user_service.fetch_all_users()
    return all_users


@router.put("/user/me", tags=["用户管理模块"], response_model=BaseUser)
async def update_user_info(user_info: BaseUser, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    """用户信息更新路由"""
    updated_user = user_service.update_user_info(current_user.id, user_info)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.post("/user/reset-password", tags=["用户管理模块"])
async def reset_user_password(user_email: EmailStr = None, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    """密码重置路由"""
    if not current_user.is_admin:
        if user_email == current_user.email or user_email is None:
            user_email = current_user.email
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    else:
        if user_email is None:
            raise HTTPException(status_code=400, detail="Email not provided")
    user_service.reset_password(user_email)
    return {"message": "Password reset request sent"}
