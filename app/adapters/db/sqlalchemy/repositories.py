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

    async def find(self, email: str) -> models.User:
        res = await self.session.execute(
            select(models.User).where(models.User.email == email).limit(1)
        )
        return res.scalars().first()

    async def remove(self, email: str) -> None:
        await self.session.execute(delete(models.User).where(models.User.email == email))

    async def list(self) -> list[models.User]:
        res = await self.session.execute(select(models.User))
        return res.scalars().all()
