from classy_fastapi import Routable, get, post
from kink import di, inject

from app.services.user import UserCrudService, UserViewService, dtos


@inject()
class UserRoutes(Routable):
    crud_service: UserCrudService
    view_service: UserViewService

    def __init__(self, crud_service: UserCrudService, view_service: UserViewService):
        super().__init__()
        self.crud_service = crud_service
        self.view_service = view_service

    @get("/")
    async def list_users(self):
        return await self.view_service.list_users()

    @post("/")
    async def create_user(self, create_user: dtos.CreateUser):
        return await self.crud_service.create_user(create_user)


user_routes = di[UserRoutes]
