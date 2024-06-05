from kink import di

from app.config import config

from .connection import Connection

# register adapters for DI
match config.ENVIRONMENT:
    case "local":
        from .cache.memory import *
        from .db.sqlalchemy import *
        from .publisher.memory import *
    case _:
        from .cache.redis import *
        from .db.sqlalchemy import *
        from .publisher.nats import *

# establish connections

class Connections:
    @classmethod
    async def create_connections(cls):
        connections: list[Connection] = di[Connection]
        for connection in connections:
            await connection.connect()
    
    @classmethod
    async def cloud_connections(cls):
        connections: list[Connection] = di[Connection]
        for connection in connections:
            await connection.close()