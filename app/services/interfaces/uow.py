from abc import ABC, abstractmethod

from app.models import User


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def find(self, email: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self, email: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def list(self) -> list[User]:
        raise NotImplementedError


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
