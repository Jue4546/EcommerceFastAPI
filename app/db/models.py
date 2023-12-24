# db/models.py 创建一个 SQLAlchemy 模型，用于映射数据库中的订单数据


from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from app.models.order.order_status import OrderStatus

Base = declarative_base()


class OrderDB(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatus))
    # 其它订单字段...

    def __repr__(self):
        return f'<Order {self.id}>'



