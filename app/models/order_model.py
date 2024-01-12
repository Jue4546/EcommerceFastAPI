"""订单模型"""
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class OrderStatus(Enum):
    PENDING_PAYMENT = ("待支付", 1)
    PROCESSING = ("处理中", 2)
    PAID = ("已支付", 3)
    PACKING = ("已发货", 4)
    IN_TRANSIT = ("运输中", 5)
    SHIPPED = ("已收货", 6)
    DELIVERED = ("已交付", 7)
    COMPLETED = ("已完成", 8)
    CANCELED = ("已取消", 9)
    RETURNED = ("已退货", 10)
    REFUNDED = ("已退款", 11)
    REFUND_FAILED = ("退款失败", 12)
    REFUND_SUCCESS = ("退款成功", 13)
    REFUND_PENDING = ("退款中", 14)
    REFUND_REJECTED = ("退款被拒绝", 15)
    REFUND_CANCELED = ("退款取消", 16)

    @classmethod
    def is_valid_status(cls, status):
        # 判断状态是否有效
        # 此方法返回一个布尔值，表示传入的状态是否存在于'OrderStatus'类的字典中
        return status in cls.__dict__.values()

    def __new__(cls, label, value):
        member = object.__new__(cls)
        member._value_ = value
        member.label = label
        return member


class Order(BaseModel):
    id: int  # 订单id
    user_id: int  # 与订单关联的用户id
    product_id: List[int]  # 与订单关联的产品id
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]
    status: OrderStatus
    address_id: int

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: OrderStatus  # 订单状态

    class Config:
        from_attributes = True


class OrderInDB(Order):
    id: int  # 订单id
    user_id: int  # 订单关联的用户id
    product_id: int  # 订单关联的产品id
    status: OrderStatus  # 订单状态
    created_at: str  # 订单创建时间
    updated_at: str  # 订单更新时间

    class Config:
        from_attributes = True


class OrderInResponse(Order):
    pass


class OrderDetailInResponse(BaseModel):
    goods_id: int
    unit_price: float
    quantity: int


class OrderWithDetails(BaseModel):
    id: int
    user_id: int
    total_price: float
    address_id: int
    order_status: OrderStatus
    created_at: str
    processed_at: str
    order_detail: List[OrderDetailInResponse]

    class Config:
        from_attributes = True