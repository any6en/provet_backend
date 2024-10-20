from sqlalchemy import Column, Integer, String, Date, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from models.model import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    avatar = Column(String(255))
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
