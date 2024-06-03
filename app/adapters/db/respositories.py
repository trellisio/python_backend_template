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
