from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from cart_model import FlowerInfo
from table_model import User,Address
Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True,comment='订单编号')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False,comment='用户ID')
    total_amount = Column(Float, nullable=False,comment='订单总价')
    #这个数据类型写这个还是Address呢
    address = Column(String, ForeignKey('addresses.id'), nullable=False, comment='收货地址')
    #支付方式没写
    created_at = Column(DateTime, server_default=func.now(), comment='下单时间')
    order_status = Column(Integer, default=0, nullable=False,comment='订单状态')  # 0: 待处理, 1: 已处理
    processed_at = Column(DateTime, nullable=True,comment='订单处理时间')  #NULL(空值)表示未处理
    # 关联用户、订单详情、收货地址
    user = relationship('Order_User', back_populates='order')
    order_details = relationship('OrderDetail', back_populates='order')
    addresses=relationship('Order_address',back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False,comment='订单编号')
    flower_id = Column(Integer, ForeignKey('flowerinfo.id'), nullable=False,comment='鲜花id')
    unit_price = Column(Float,nullable=False,comment='鲜花单价')
    quantity = Column(Integer, nullable=False,comment='鲜花数量')
    # 其他订单详情信息字段...
    order = relationship('Order', back_populates='order_details')
    flower = relationship('Order_flowerInfo', back_populates='order_details')

class Order_user(User):
    order=relationship('Order',back_populates='user')

class Order_flowerInfo(FlowerInfo):
    order_details=relationship('OrderDetail',back_populates='flower')

class Order_address(Address):
    order=relationship('Order',back_populates='addresses')



