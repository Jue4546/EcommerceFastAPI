"""用户模型"""
from typing import Union, Optional

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


# 用户地址模型
class AddressBase(BaseModel):
    province: str
    city: str
    district: str
    street: str
    postal_code: str
    detail: str
    is_default: bool


"""
这样的Pydantic模型可以用于API端点的请求和响应验证。
在路由处理函数中，你可以使用AddressCreate来验证创建请求，
AddressUpdate来验证更新请求，而Address则可以用于返回。
"""


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    user_id: int
    is_default: Optional[bool]

    class Config:
        orm_mode = True


"""
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
