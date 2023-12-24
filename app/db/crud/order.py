# db/crud/order.py

from sqlalchemy.orm import Session
from app.models.order.order_status import OrderStatus
from app.db.models import OrderDB


def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    # 在数据库中更新订单状态
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()

    if db_order:
        db_order.status = new_status
        db.commit()

    return db_order
