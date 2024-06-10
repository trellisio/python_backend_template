from kink import inject

from app.models import User

from ..interfaces import Uow
from .dtos import CreateUser


@inject()
class UserService:
    uow: Uow
    
    def __init__(self, uow: Uow):
        self.uow = uow
    
    async def create_user(self, create_user: CreateUser):
        async with self.uow:
            user = User(email=create_user.email)
            await self.uow.user_repository.add(user)
            await self.uow.commit()