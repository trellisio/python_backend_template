from kink import inject

from app.domain.models import User

from ..adapters import Publisher, Uow
from ..errors import NoResourceException, ResourceExistsException
from .dtos import CreateUser


@inject()
class UserCrudService:
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


@inject()
class UserService:
    uow: Uow
    publisher: Publisher

    def __init__(self, uow: Uow, publisher: Publisher):
        self.uow = uow
        self.publisher = publisher

    async def do_something_domainy(self, email: str):
        async with self.uow:
            users = await self.uow.user_repository.find(email)
            if not users:
                raise NoResourceException()

            for user in users:
                user.some_domain_method()

            await self.uow.commit()
