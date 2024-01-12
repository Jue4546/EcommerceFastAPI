from typing import List

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.db.base import SessionLocal
from app.models.cart_model import CartItem, CartItemBase


class CartItemCreationError(Exception):
    pass


def create_or_update_cart_item_db(cart_item: CartItemBase) -> CartItem:
    """创建或更新购物车项并将其添加到数据库"""
    db = SessionLocal()
    try:
        update_query = text('UPDATE "cart" SET amount = amount + :amount '
                            'WHERE goods_id = :goods_id AND user_id = :user_id '
                            'RETURNING *')
        db_cart_item = db.execute(update_query, {
            'goods_id': cart_item.goods_id,
            'amount': cart_item.amount,
            'user_id': cart_item.user_id,
        }).fetchone()

        if db_cart_item:
            db.commit()
            return CartItem(id=db_cart_item[0],
                            user_id=db_cart_item[1],
                            goods_id=db_cart_item[2],
                            amount=db_cart_item[3],
                            created_at=str(db_cart_item[4]),
                            updated_at=str(db_cart_item[5]))

        insert_query = text('INSERT INTO "cart" (goods_id, amount, user_id) VALUES '
                            '(:goods_id, :amount, :user_id) RETURNING *')
        db_cart_item = db.execute(insert_query, {
            'goods_id': cart_item.goods_id,
            'amount': cart_item.amount,
            'user_id': cart_item.user_id,
        }).fetchone()
        db.commit()

        if db_cart_item:
            return CartItem(id=db_cart_item[0],
                            user_id=db_cart_item[1],
                            goods_id=db_cart_item[2],
                            amount=db_cart_item[3],
                            created_at=str(db_cart_item[4]),
                            updated_at=str(db_cart_item[5]))
        else:
            return None
    except IntegrityError as e:
        db.rollback()
        db.close()
        if "violates foreign key constraint" in str(e):
            raise CartItemCreationError("Invalid goods_id. This product does not exist.")
        else:
            raise e


def get_cart_item_db(item_id: int, owner_id: int) -> CartItem:
    """根据购物车项ID从数据库中获取购物车项信息"""
    db = SessionLocal()
    select_query = text('SELECT id, goods_id, amount, user_id, created_at, updated_at FROM "cart" '
                        'WHERE id = :item_id AND user_id = :user_id')
    db_cart_item = db.execute(select_query, {'item_id': item_id, 'user_id': owner_id}).fetchone()
    db.close()
    if db_cart_item:
        return CartItem(
            id=db_cart_item[0],
            goods_id=db_cart_item[1],
            amount=db_cart_item[2],
            user_id=db_cart_item[3],
            created_at=str(db_cart_item[4]),
            updated_at=str(db_cart_item[5])
        )
    else:
        return None


def get_cart_items_db(owner_id: int, skip: int = 0, limit: int = 10) -> List[CartItem]:
    """从数据库中获取购物车所有项信息"""
    db = SessionLocal()
    select_all_query = text('SELECT id, goods_id, amount, user_id FROM "cart" '
                            'WHERE user_id = :user_id LIMIT :limit OFFSET :skip')
    cart_items_data = db.execute(select_all_query, {'limit': limit, 'skip': skip, 'user_id': owner_id}).fetchall()
    db.close()
    cart_items_db = [
        CartItem(
            id=item_tuple[0],
            goods_id=item_tuple[1],
            amount=item_tuple[2],
            user_id=item_tuple[3]
        )
        for item_tuple in cart_items_data
    ]
    return cart_items_db


def update_cart_item_db(cart_item: CartItemBase) -> CartItem:
    """更新购物车项信息到数据库"""
    db = SessionLocal()
    update_query = text('UPDATE "cart" SET amount = :amount, updated_at = CURRENT_TIMESTAMP '
                        'WHERE goods_id = :goods_id AND user_id = :user_id RETURNING *')
    db_cart_item = db.execute(update_query, {
        'goods_id': cart_item.goods_id,
        'amount': cart_item.amount,
        'user_id': cart_item.user_id
    }).fetchone()
    db.commit()

    if db_cart_item:
        return CartItem(
            id=db_cart_item[0],
            user_id=db_cart_item[1],
            goods_id=db_cart_item[2],
            amount=db_cart_item[3],
            created_at=str(db_cart_item[4]),
            updated_at=str(db_cart_item[5])
        )
    else:
        return None


def delete_cart_item_db(goods_id: int, user_id: int) -> bool:
    """从数据库中删除购物车中的商品"""
    db = SessionLocal()
    delete_query = text('DELETE FROM "cart" WHERE goods_id = :goods_id AND user_id = :user_id RETURNING *')
    db_cart_item = db.execute(delete_query, {'goods_id': goods_id, 'user_id': user_id}).fetchone()
    db.commit()
    db.close()
    if db_cart_item is None:
        return False
    else:
        return True

