from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class Hospital(Base):
    __tablename__="patients"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(90),nullable=False)
    department=Column(String(80),nullable=False)
    location=Column(String(70),nullable=False)
    address=Column(String(100),nullable=True)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    password = Column(String(300), nullable=False) 