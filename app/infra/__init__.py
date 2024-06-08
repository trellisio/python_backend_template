from kink import di

from app.config import config

from .connection import Connection

# Initialize Infra
match config.ENVIRONMENT:
    case "local":
        from .memory.cache import *
        from .memory.publisher import *
        from .sqlalchemy.uow import *
    case _:
        from .nats.publisher import *
        from .redis.cache import *
        from .sqlalchemy.uow import *


async def init_connections():
    connections: list[Connection] = di[Connection]
    for connection in connections:
        await connection.connect()


async def close_connections(cleanup: bool = False):
    connections: list[Connection] = di[Connection]
    for connection in connections:
        await connection.close(cleanup)
