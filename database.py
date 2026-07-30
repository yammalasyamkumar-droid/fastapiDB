from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL="mysql+pymysql://avnadmin:AVNS_GP8uTeG-MEbQfk0__mq@mysqldb-yammalasyamkumar-backend.f.aivencloud.com:17963/defaultdb"
engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base=declarative_base()
