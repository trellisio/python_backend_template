from kink import di, inject

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


@inject()
class InfraInitializer:
    connections: list[Connection]

    def __init__(self, connections: list[Connection]):
        self.connections = connections

    async def init_connections(self):
        for connection in self.connections:
            await connection.connect()

    async def close_connections(self, cleanup: bool = False):
        for connection in self.connections:
            await connection.close(cleanup)


infra_initializer = di[InfraInitializer]

init_connections = lambda: infra_initializer.init_connections()
close_connections = lambda: infra_initializer.close_connections()
