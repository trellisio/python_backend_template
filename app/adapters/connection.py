from abc import ABC, abstractmethod

from kink import inject


class Connection(ABC):
    @abstractmethod
    async def connect():
        pass

    @abstractmethod
    async def close(cleanup: bool = False):
        pass


@inject()
class Connections:
    connections: list[Connection]

    def __init__(self, connections: list[Connection]):
        self.connections = connections

    async def create_connections(self):
        for connection in self.connections:
            await connection.connect()

    async def close_connections(self):
        for connection in self.connections:
            await connection.close()
