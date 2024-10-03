from fastapi import APIRouter

from .monitoring import monitoring_routes
from .user import user_routes

router = APIRouter()
v1_router = APIRouter(prefix="/v1")

# monitoring
router.include_router(monitoring_routes.router)

# v1
v1_router.include_router(user_routes.router, prefix="/users")

# main
router.include_router(v1_router)
