"""用户模型"""
from pydantic import BaseModel, EmailStr
from typing import Union, Optional, List


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


"""
# 用户地址模型
class Address(BaseModel):
    street: str
    city: str
    state: str
    detail: str


# 用户个人资料模型
class UserProfile(BaseModel):
    full_name: str
    date_of_birth: str  # 可以使用 datetime 类型
    phone_number: Optional[str] = None
    addresses: List[Address] = []


# 用户认证信息模型
class UserAuth(BaseModel):
    username: str
    email: str
    hashed_password: str


# 用户订单历史模型
class OrderHistory(BaseModel):
    order_id: str
    total_amount: float
    items: List[str]
    # 其他订单相关信息


# 全面的用户类，包含个人资料、认证信息和订单历史
class User(BaseModel):
    profile: UserProfile
    auth: UserAuth
    order_history: List[OrderHistory] = []
"""