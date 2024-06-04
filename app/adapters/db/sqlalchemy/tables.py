from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, nullable=False, unique=True, index=True),
)
