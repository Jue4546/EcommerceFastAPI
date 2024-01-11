"""购物车路由：api/cart_route.py"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.cart_model import CartItem, CartItemBase as CartItemCreate, CartItemBase as CartItemUpdate
from app.models.user_model import *
from app.services import cart_service, auth_service

router = APIRouter()

# 同样，这里只是简单示例，你可以根据实际需求进行修改


@router.post("/cart/items", tags=["购物车管理"])
async def create_cart_item(cart_item: CartItemCreate, current_user: UserInDB = Depends(auth_service.get_current_user)):
    return cart_service.create_cart_item(cart_item, current_user)


@router.get("/cart/items/{item_id}", tags=["购物车管理"])
async def get_cart_item(item_id: int, current_user: UserInDB = Depends(auth_service.get_current_user)):
    db_cart_item = cart_service.get_cart_item(item_id)
    if db_cart_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to access this cart item")
    return db_cart_item


@router.get("/cart/items", tags=["购物车管理"], response_model=List[CartItem])
async def get_cart_items(skip: int = 0, limit: int = 10, current_user: UserInDB = Depends(auth_service.get_current_user)):
    return cart_service.get_cart_items(skip=skip, limit=limit, owner_id=current_user.id)


@router.put("/cart/items/{item_id}", tags=["购物车管理"])
async def update_cart_item(item_id: int, cart_item: CartItemUpdate, current_user: UserInDB = Depends(auth_service.get_current_user)):
    db_cart_item = cart_service.get_cart_item(item_id)
    if db_cart_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to update this cart item")
    return cart_service.update_cart_item(item_id, cart_item)


@router.delete("/cart/items/{item_id}", tags=["购物车管理"])
async def delete_cart_item(item_id: int, current_user: UserInDB = Depends(auth_service.get_current_user)):
    db_cart_item = cart_service.get_cart_item(item_id)
    if db_cart_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not permitted to delete this cart item")
    return cart_service.delete_cart_item(item_id)
