"""购物车服务逻辑：service/cart_service.py"""
from typing import List

from app.models.cart_model import CartItem, CartItemBase
from app.db.crud.cart_crud import create_or_update_cart_item_db, get_cart_item_db, get_cart_items_db, update_cart_item_db, \
    delete_cart_item_db, CartItemCreationError


def create_cart_item(cart_item: CartItemBase) -> CartItem:
    """创建购物车项服务逻辑"""
    try:
        return create_or_update_cart_item_db(cart_item)
    except CartItemCreationError as e:
        raise e


def get_cart_item(item_id: int, owner_id: int) -> CartItem:
    """获取购物车项服务逻辑"""
    return get_cart_item_db(item_id, owner_id)


def get_cart_items(owner_id: int, skip: int = 0, limit: int = 10) -> List[CartItem]:
    """获取购物车所有项服务逻辑"""
    return get_cart_items_db(owner_id, skip, limit)


def update_cart_item(cart_item: CartItemBase) -> CartItem:
    """更新购物车项服务逻辑"""
    return update_cart_item_db(cart_item)


def delete_cart_item(goods_id: int, user_id: int) -> bool:
    """删除购物车中的商品服务逻辑"""
    return delete_cart_item_db(goods_id, user_id)
