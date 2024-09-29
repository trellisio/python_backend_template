from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()


@router.get("/healthz")
async def healthz():
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/metrics")
async def metrics():
    return Response(status_code=HTTP_204_NO_CONTENT)
