from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func,Text,Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from table_model import User
Base = declarative_base()

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) #主键自增
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID')
    flower_id = Column(String(100), ForeignKey('flowerinfo.id'), nullable=False, comment='鲜花ID')
    amount = Column(Integer(99),nullable=False,comment='商品数量')
    total_price = Column(Integer, nullable=False, comment='商品总价')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    #关联鲜花信息
    flower = relationship('FlowerInfo', back_populates='carts')
    user = relationship('Flower_User', back_populates='carts')



    __mapper_args__ = {"order_by": flower}  # 默认是正序，倒序加上.desc()方法


class FlowerInfo(Base):
    __tablename__ = 'flowerinfo'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='鲜花id')
    name = Column(String(50), unique=True, nullable=False, comment='商品名称')
    amount = Column(Integer, nullable=False, comment='商品数量')
    unit_price = Column(Float, nullable=False, comment='商品单价')
    description = Column(Text, comment='鲜花描述')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    # 关联图片
    images = relationship("FlowerImage", back_populates="flower_info")
    # 关联购物车
    carts = relationship('Cart', back_populates='flower')

    __mapper_args__ = {"order_by": unit_price}  # 默认是升序


class FlowerImage(Base):
    __tablename__ = 'flowerimage'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_path = Column(String(255), nullable=False, comment='图片路径')
    flower_info_id = Column(Integer, ForeignKey('flowerinfo.id'))
    #back_populates来指定反向访问的属性名称
    flower_info = relationship("FlowerInfo", back_populates="images")

class Flower_User(User):
    carts = relationship('Cart', back_populates='user')



