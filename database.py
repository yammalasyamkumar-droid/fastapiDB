from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")

<<<<<<< HEAD
=======
DATABASE_URL="mysql+pymysql://avnadmin:AVNS_GP8uTeG-MEbQfk0__mq@mysqldb-yammalasyamkumar-backend.f.aivencloud.com:17963/defaultdb"
>>>>>>> d926fb3701414f62b45a392e3bc4fa61a04de4ff
engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base=declarative_base()
