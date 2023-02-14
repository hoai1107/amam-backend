from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

RDS_POSTGRESQL_URL = os.getenv("RDS_POSTGRESQL_URL")
RDS_MASTER_USERNAME = os.getenv("RDS_MASTER_USERNAME")
RDS_MASTER_PASSWORD = os.getenv("RDS_MASTER_PASSWORD")

DATABASE_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=RDS_MASTER_USERNAME,
    password=RDS_MASTER_PASSWORD,
    host=RDS_POSTGRESQL_URL,
    port=5432,
    database="amam",
)

# DATABASE_URL = "postgresql://postgres:123456@localhost:5432/amam"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
