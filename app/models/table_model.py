from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# 创建基本映射类
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_disabled = Column(Boolean, default=False)
    registration_time = Column(DateTime, default=datetime.now)
    last_login_time = Column(DateTime)

    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    country = Column(String(100))
    province_or_state = Column(String(100))
    city = Column(String(100))
    street = Column(String(255))
    postal_code = Column(String(20))
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")


class VerificationCode(Base):
    __tablename__ = 'verification_codes'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    code = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
