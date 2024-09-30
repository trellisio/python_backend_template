from fastapi import APIRouter

from .monitoring import router as monitoring_router
from .user import user_routes

router = APIRouter()
v1_router = APIRouter(prefix="/v1")
router.include_router(v1_router)

# monitoring
router.include_router(monitoring_router)

# v1
v1_router.include_router(user_routes.router, prefix="/users")
