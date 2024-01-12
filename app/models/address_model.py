"""用户地址模型"""
from typing import Union, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


class AddressBase(BaseModel):
    user_id: int
    province_or_state: str
    city: str
    district: str
    street: str
    postal_code: str
    detail: str
    is_default: bool = False


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
        from_attributes = True

