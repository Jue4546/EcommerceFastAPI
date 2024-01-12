from typing import List

from app.db.crud.order_crud import create_order_db, get_order_db, get_orders_db, update_order_db, delete_order_db
from app.models.order_model import OrderCreate, OrderUpdate, OrderInResponse, OrderWithDetails


def create_order(order_create: OrderCreate) -> OrderInResponse:
    return create_order_db(order_create)


def get_order(order_id: int) -> OrderWithDetails:
    return get_order_db(order_id)


def get_orders(skip: int = 0, limit: int = 10) -> List[OrderInResponse]:
    return get_orders_db(skip=skip, limit=limit)


def update_order(order_id: int, order_update: OrderUpdate) -> OrderInResponse:
    return update_order_db(order_id, order_update)


def delete_order(order_id: int) -> OrderInResponse:
    return delete_order_db(order_id)
