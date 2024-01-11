"""订单路由：api/order_route.py"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.order_model import Order, OrderBase as OrderCreate, OrderBase as OrderUpdate
from app.services import order_service, auth_service

router = APIRouter()

# 你可以根据具体的业务逻辑修改以下路由


@router.post("/orders", tags=["订单管理"])
async def create_order(order: OrderCreate, current_user: User = Depends(auth_service.get_current_user)):
    return order_service.create_order(order, current_user)


@router.get("/orders/{order_id}", tags=["订单管理"])
async def get_order(order_id: int, current_user: User = Depends(auth_service.get_current_user)):
    db_order = order_service.get_order(order_id)
    if db_order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to access this order")
    return db_order


@router.get("/orders", tags=["订单管理"], response_model=List[Order])
async def get_orders(skip: int = 0, limit: int = 10, current_user: User = Depends(auth_service.get_current_user)):
    return order_service.get_orders(skip=skip, limit=limit, owner_id=current_user.id)


@router.put("/orders/{order_id}", tags=["订单管理"])
async def update_order(order_id: int, order: OrderUpdate, current_user: User = Depends(auth_service.get_current_user)):
    db_order = order_service.get_order(order_id)
    if db_order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to update this order")
    return order_service.update_order(order_id, order)


@router.delete("/orders/{order_id}", tags=["订单管理"])
async def delete_order(order_id: int, current_user: User = Depends(auth_service.get_current_user)):
    db_order = order_service.get_order(order_id)
    if db_order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to delete this order")
    return order_service.delete_order(order_id)
