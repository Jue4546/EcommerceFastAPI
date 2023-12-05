"""用户模型"""
from pydantic import BaseModel, EmailStr
from typing import Union


class BaseUser(BaseModel):
    """用户基本信息"""
    username: str
    email: Union[EmailStr, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = False
    admin: Union[bool, None] = False


class RegisterUser(BaseUser):
    password: str
    hashed_password: Union[str, None] = None


class UserInDB(BaseUser):
    """表示数据库中实际存储的用户模型"""
    id: int
    hashed_password: str

