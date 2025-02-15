from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:9601@localhost:3306/core_fastapi")

meta = MetaData()
conn = engine.connect()
