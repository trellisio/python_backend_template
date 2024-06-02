from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models

from ..respositories import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, User: models.User) -> None:
        self.session.add(User)

    async def find(self, name: str) -> models.User:
        res = await self.session.execute(
            select(models.User).where(models.User.name == name).limit(1)
        )
        return res.scalars().first()

    async def remove(self, name: str) -> None:
        await self.session(delete(models.User).where(models.User.name == name))

    async def list(self) -> list[models.User]:
        res = await self.session.execute(select(models.User))
        return res.scalars().all()
