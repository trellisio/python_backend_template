from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()

board = Table(
    "board",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True),
)
