from typing import Optional

from pydantic import BaseModel


class CartItemBase(BaseModel):
    user_id: int
    goods_id: int
    amount: int


class CartItem(CartItemBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

