from kink import di

from app.connections import Connection

from .config import config

# Adapters
match config.ENVIRONMENT:
    case "local":
        from app.adapters.cache.memory import *
        from app.adapters.db.sqlalchemy import *
        from app.adapters.publisher.memory import *
    case _:
        from app.adapters.cache.redis import *
        from app.adapters.db.sqlalchemy import *
        from app.adapters.publisher.nats import *
        
# Connections    
match config.ENVIRONMENT:
    case "local":
        from app.connections.sql.sqlite import *
    case _:
        from app.connections.sql.postgres import *

async def init_connections():
    connections: list[Connection] = di[Connection]
    for connection in connections:
        await connection.connect()


async def close_connections(cleanup: bool = False):
    connections: list[Connection] = di[Connection]
    for connection in connections:
        await connection.close(cleanup)