"""订单模块路由：api/order_route.py"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.order_model import OrderCreate, OrderUpdate, OrderInResponse, OrderWithDetails, OrderStatus
from app.services.order_service import create_order, get_order, get_orders, update_order, delete_order
from models.user_model import UserInDB
from services import auth_service, address_service

router = APIRouter()


@router.post("/orders/", response_model=OrderInResponse, tags=["订单管理模块"])
async def create_new_order(product_ids: List[int], address_id: int = None, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    if address_id is None:
        address_id = address_service.get_default_address_id(current_user.id)
    order_create = OrderCreate(
        user_id=current_user.id,
        product_ids=product_ids,
        status=OrderStatus.PENDING_PAYMENT,
        address_id=address_id
    )

    return create_order(order_create)


@router.get("/orders/{order_id}", response_model=OrderWithDetails, tags=["订单管理模块"])
async def read_order(order_id: int):
    return get_order(order_id)


@router.get("/orders/", response_model=List[OrderInResponse], tags=["订单管理模块"])
async def read_orders(skip: int = 0, limit: int = 10):
    return get_orders(skip=skip, limit=limit)


@router.put("/orders/{order_id}", response_model=OrderInResponse, tags=["订单管理模块"])
async def update_existing_order(order_id: int, order_update: OrderUpdate):
    return update_order(order_id, order_update)


@router.delete("/orders/{order_id}", response_model=OrderInResponse, tags=["订单管理模块"])
async def delete_existing_order(order_id: int):
    return delete_order(order_id)
