from kink import inject

from app.domain.models import User

from ..adapters import Uow
from ..errors import ResourceExistsException
from .dtos import CreateUser


@inject()
class UserService:
    uow: Uow

    def __init__(self, uow: Uow):
        self.uow = uow

    async def create_user(self, create_user: CreateUser):
        async with self.uow:
            users = await self.uow.user_repository.find(create_user.email)
            if users:
                raise ResourceExistsException()

            user = User(email=create_user.email)
            await self.uow.user_repository.add(user)
            await self.uow.commit()
