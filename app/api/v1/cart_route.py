"""购物车路由：api/cart_route.py"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.cart_model import CartItem, CartItemBase as CartItemCreate, CartItemBase as CartItemUpdate
from app.models.user_model import *
from app.services import cart_service, auth_service

router = APIRouter()


@router.post("/cart/items", tags=["购物车管理"])
async def create_cart_item(goods_id, amount, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    try:
        cart_item = CartItemCreate(
            user_id=current_user.id,
            goods_id=goods_id,
            amount=amount
        )
        result = cart_service.create_cart_item(cart_item)
        if result:
            return {"message": "Cart item created successfully", "cart_item": result}
        else:
            raise HTTPException(status_code=500, detail="Failed to create cart item")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cart/items/{item_id}", tags=["购物车管理"], response_model=CartItem)
async def get_cart_item(item_id: int, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    return cart_service.get_cart_item(item_id, current_user.id)


@router.get("/cart/items", tags=["购物车管理"], response_model=List[CartItem])
async def get_cart_items(skip: int = 0, limit: int = 10,
                         current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    return cart_service.get_cart_items(skip=skip, limit=limit, owner_id=current_user.id)


@router.put("/cart/items/{item_id}", tags=["购物车管理"])
async def update_cart_item(cart_item: CartItemUpdate,
                           current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    admin = current_user.is_admin
    if cart_item.user_id != current_user.id and not admin:
        cart_item.user_id = current_user.id
    return cart_service.update_cart_item(cart_item)


@router.delete("/cart/items/{goods_id}", tags=["购物车管理"])
async def delete_cart_item(goods_id: int, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    success = cart_service.delete_cart_item(goods_id, current_user.id)
    if success:
        return {"message": "Cart item deleted successfully"}
    else:
            raise HTTPException(status_code=404, detail="Cart item not found")
