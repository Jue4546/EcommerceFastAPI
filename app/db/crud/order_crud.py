from datetime import datetime
from typing import List

from sqlalchemy import text

from app.db.base import SessionLocal
from app.models.order_model import Order, OrderCreate, OrderUpdate, OrderInResponse, OrderWithDetails, \
    OrderDetailInResponse, OrderStatus


def create_order_db(order_create: OrderCreate) -> OrderInResponse:
    db = SessionLocal()

    # 1. 获取购物车中商品的数量和对应的商品信息
    select_query = text('SELECT c.goods_id, c.amount, g.unit_price FROM cart c '
                        'JOIN goods_info g ON c.goods_id = g.id '
                        'WHERE c.user_id = :user_id AND c.goods_id = ANY(:product_ids)')

    cart_items = db.execute(
        select_query,
        {
            'user_id': order_create.user_id,
            'product_ids': order_create.product_ids,
        }
    ).fetchall()

    # 2. 计算订单总金额
    total_price = sum(amount * unit_price for amount, unit_price, stock in cart_items)

    # 3. 创建订单
    insert_query_order = text('INSERT INTO "order" (user_id, total_price, address_id, order_status, created_at) '
                              'VALUES (:user_id, :total_price, :address_id, :order_status, :created_at) RETURNING *')
    db_order = db.execute(
        insert_query_order,
        {
            'user_id': order_create.user_id,
            'total_price': total_price,
            'address_id': order_create.address_id,
            'order_status': order_create.status.value,
            'created_at': datetime.now()
        }
    ).fetchone()

    # 4. 将商品详情插入订单详情表
    insert_query_detail = text('INSERT INTO order_detail (order_id, goods_id, unit_price, quantity) '
                               'VALUES (:order_id, :goods_id, :unit_price, :quantity)')

    for amount, unit_price, stock in cart_items:
        check_quantity = min(amount, stock)
        if check_quantity > 0:
            db.execute(
                insert_query_detail,
                {
                    'order_id': db_order[0],
                    'goods_id': order_create.product_ids[cart_items.index((amount, unit_price, stock))],
                    'unit_price': unit_price,
                    'quantity': check_quantity
                }
            )
        else:
            raise ValueError(f"商品 {order_create.product_ids[cart_items.index((amount, unit_price, stock))]} 库存不足")

    # 5. 减少库存
    for amount, unit_price, stock in cart_items:
        check_quantity = min(amount, stock)
        goods_id = order_create.product_ids[cart_items.index((amount, unit_price, stock))]

        # 更新商品信息表中的库存
        update_stock_query = text('UPDATE goods_info SET amount = amount - :quantity WHERE id = :goods_id')
        db.execute(update_stock_query, {'quantity': check_quantity, 'goods_id': goods_id})

    # 6. 删除购物车中的商品
    delete_cart_query = text('DELETE FROM cart WHERE user_id = :user_id AND goods_id = ANY(:product_ids)')
    db.execute(delete_cart_query, {'user_id': order_create.user_id, 'product_ids': order_create.product_ids})

    db.commit()

    # 7. 返回带有商品详情的订单信息
    order = OrderInResponse(
        id=db_order[0],
        user_id=db_order[1],
        total_price=db_order[2],
        address_id=db_order[3],
        created_at=db_order[4].strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=db_order[4].strftime("%Y-%m-%d %H:%M:%S"),
        product_id=order_create.product_ids,
        status=order_create.status,
    )

    return order


def get_order_db(order_id: int) -> OrderWithDetails:
    db = SessionLocal()
    select_query = text(
        'SELECT o.id, o.user_id, o.total_price, o.address_id, o.order_status, o.created_at, o.processed_at, '
        'od.goods_id, od.unit_price, od.quantity '
        'FROM "order" o '
        'JOIN "order_detail" od ON o.id = od.order_id '
        'WHERE o.id = :order_id')
    db_order = db.execute(select_query, {'order_id': order_id}).fetchone()
    db.close()
    if db_order:
        return OrderWithDetails(**dict(db_order))
    else:
        return None


def get_orders_db(skip: int = 0, limit: int = 10) -> List[OrderInResponse]:
    db = SessionLocal()
    select_all_query = text('SELECT id, user_id, total_price, address_id, order_status, created_at, processed_at '
                            'FROM "order" LIMIT :limit OFFSET :skip')
    orders_data = db.execute(select_all_query, {'limit': limit, 'skip': skip}).fetchall()
    db.close()
    orders_db = [
        OrderInResponse(
            id=order_tuple[0],
            user_id=order_tuple[1],
            total_price=order_tuple[2],
            address_id=order_tuple[3],
            order_status=order_tuple[4],
            created_at=order_tuple[5],
            processed_at=order_tuple[6],
        )
        for order_tuple in orders_data
    ]
    return orders_db


def update_order_db(order_id: int, order_update: OrderUpdate) -> OrderInResponse:
    db = SessionLocal()
    update_query = text('UPDATE "order" SET order_status = :order_status '
                        'WHERE id = :order_id RETURNING *')
    db_order = db.execute(
        update_query,
        {
            'order_status': order_update.order_status.value,
            'order_id': order_id,
        },
    ).fetchone()
    db.commit()

    order_with_details = get_order_with_details(db_order['id'])

    db.close()
    return order_with_details


def delete_order_db(order_id: int) -> OrderInResponse:
    db = SessionLocal()
    delete_query = text('DELETE FROM "order" WHERE id = :order_id RETURNING *')
    db_order = db.execute(delete_query, {'order_id': order_id}).fetchone()
    db.commit()

    # Additional logic to get order details
    order_with_details = get_order_with_details(db_order['id'])

    db.close()
    return order_with_details


def get_order_with_details(order_id: int) -> OrderWithDetails:
    db = SessionLocal()
    select_details_query = text(
        'SELECT o.id, o.user_id, o.total_price, o.address_id, o.order_status, o.created_at, o.processed_at, '
        'od.goods_id, od.unit_price, od.quantity '
        'FROM "order" o '
        'JOIN "order_detail" od ON o.id = od.order_id '
        'WHERE o.id = :order_id')
    db_order = db.execute(select_details_query, {'order_id': order_id}).fetchone()
    db.close()
    if db_order:
        return OrderWithDetails(**dict(db_order))
    else:
        return None
