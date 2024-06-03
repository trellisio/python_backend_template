from abc import ABC, abstractmethod

from .respositories import UserRepository


class Uow(ABC):
    user_repository: UserRepository

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

