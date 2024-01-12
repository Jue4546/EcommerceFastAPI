"""用户模型"""
from typing import Union, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """用户基本信息"""
    username: str
    email: Union[EmailStr, None] = None
    is_disabled: Union[bool, None] = False
    is_admin: Union[bool, None] = False


class RegisterUser(BaseUser):
    verification_code: str
    password: str
    hashed_password: Union[str, None] = None


class UserInDB(BaseUser):
    """表示数据库中实际存储的用户模型"""
    id: int
    hashed_password: Union[str, None] = None
