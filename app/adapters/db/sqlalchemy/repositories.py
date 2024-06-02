from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models

from ..respositories import BoardRepository


class SqlAlchemyBoardRepository(BoardRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, board: models.Board) -> None:
        self.session.add(board)

    async def find(self, name: str) -> models.Board:
        res = await self.session.execute(
            select(models.Board).where(models.Board.name == name).limit(1)
        )
        return res.scalars().first()

    async def remove(self, name: str) -> None:
        await self.session(delete(models.Board).where(models.Board.name == name))

    async def list(self) -> list[models.Board]:
        res = await self.session.execute(select(models.Board))
        return res.scalars().all()
