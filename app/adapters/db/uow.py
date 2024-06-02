from abc import ABC, abstractmethod

from .respositories import BoardRepository


class Uow(ABC):
    boardRepository: BoardRepository

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc, tb):
        await self.rollback()
        await self.close()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    # Views
    @abstractmethod
    async def execute(self, query: str):
        raise NotImplementedError()
