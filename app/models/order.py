# models/order.py
from __future__ import absolute_import
from order.order_status import OrderStatus

from pydantic import BaseModel


'''
'orm_mode = True' Pydantic库中的一个选项
ORM模式，将Pydantic模型转换为数据库模型
自动为模型创建一个ORM（对象关系映射）类，以便在数据库中进行操作。
Order、OrderCreate、OrderUpdate 和 OrderInResponse 类映射到数据库表，
/以便可以方便地进行数据库操作。
'''


class Order(BaseModel):
    id: int  # 订单id
    user_id: int  # 与订单关联的用户id
    product_id: int  # 与订单关联的产品id
    quantity: int  # 订单关联的产品数量
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    user_id: int            # 订单关联的用户id
    product_id: int         # 订单关联的产品id
    quantity: int           # 订单关联的产品数量
    status: OrderStatus     # 订单状态

    class Config:
        orm_mode = True


class OrderUpdate(BaseModel):
    status: OrderStatus     # 订单状态

    class Config:
        orm_mode = True


class OrderInDB(Order):
    id: int                           # 订单id
    user_id: int                      # 订单关联的用户id
    product_id: int                     # 订单关联的产品id
    quantity: int                       # 订单关联的产品数量
    status: OrderStatus                 # 订单状态
    created_at: str                     # 订单创建时间
    updated_at: str                     # 订单更新时间

    class Config:
        orm_mode = True


class OrderInResponse(Order):
    id: int                 # 订单id
    user_id: int            # 订单关联的用户id
    product_id: int         # 订单关联的产品id
    quantity: int           # 订单关联产品数量
    status: OrderStatus     # 订单状态
    created_at: str         # 订单创建时间
    updated_at: str         # 订单更新时间

    class Config:
        orm_mode = True
