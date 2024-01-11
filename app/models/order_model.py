from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    total_price: float
    address_id: int
    order_status: Optional[int] = 0


class Order(OrderBase):
    id: int
    created_at: Optional[str] = None
    processed_at: Optional[str] = None

