from fastapi import APIRouter

from .monitoring import router as monitoring_router
from .user import user_routes

router = APIRouter(prefix="/v1")

router.include_router(monitoring_router)
router.include_router(user_routes.router, prefix="/users")
