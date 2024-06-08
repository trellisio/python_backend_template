from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    async def connect():
        pass

    @abstractmethod
    async def close(cleanup: bool = False):
        pass
