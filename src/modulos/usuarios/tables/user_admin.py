from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from ....config.db import meta, engine

users = Table(
    "mod_usuarios_administradores", 
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("lastname", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("password_dencrypt", String(255))
)

meta.create_all(engine)
