from typing import Annotated

from classy_fastapi import Routable, get, post
from fastapi import Query
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
    async def list_users(
        self,
        skip: Annotated[int, Query(ge=0)],
        limit: Annotated[int, Query(le=500)],
    ):
        return await self.view_service.list_users(skip, limit)

    @post("/")
    async def create_user(self, create_user: dtos.CreateUser):
        return await self.crud_service.create_user(create_user)


user_routes = di[UserRoutes]
