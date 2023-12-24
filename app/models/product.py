# models/product.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String)


'''
__repr__ 特殊方法
当一个对象被打印时，自动调用
获取对象的表现形式，（产品对象的各个属性）
'''


def __repr__(self):
    return f"<Product(name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity}, " \
           f"category={self.category})>"
