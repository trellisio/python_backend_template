from classy_fastapi import Routable, post
from kink import di, inject

from app.services.user import UserService, dtos


@inject()
class UserRoutes(Routable):
    service: UserService
    
    def __init__(self, service: UserService):
        super().__init__()
        self.service = service
    
    @post("/")
    async def create_user(self, create_user: dtos.CreateUser):
        return await self.service.create_user(create_user)

user_routes = di[UserRoutes]