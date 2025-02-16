from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:9601@localhost:3306/core_fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()
conn = engine.connect()
