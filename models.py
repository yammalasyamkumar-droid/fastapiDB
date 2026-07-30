from sqlalchemy import Column, Integer, String
from database import Base

class Hospital(Base):
    __tablename__="patients"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(90),nullable=False)
    department=Column(String(80),nullable=False)
    location=Column(String(70),nullable=False)
    address=Column(String(100),nullable=True)
