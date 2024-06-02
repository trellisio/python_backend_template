from abc import ABC, abstractmethod

from app.models import Board


class BoardRepository(ABC):
    @abstractmethod
    async def add(self, board: Board) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def find(self, name: str) -> Board:
        raise NotImplementedError()

    @abstractmethod
    async def remove(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def list(self) -> list[Board]:
        raise NotImplementedError
