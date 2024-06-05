from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings

from app.adapters import Connections
from app.logger import logger

from .routers import router


class FastApiConfig(BaseSettings):
    FASTAPI_ENV: str = Field(
        description="Environment server is running in", default="development"
    )
    PORT: int = Field(description="Port for server", default=8000)
    URL_PREFIX: str = Field(description="URL to prefix routes on server", default="")


config = FastApiConfig()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Connections.create_connections()
    # add routes to server
    app.include_router(router, prefix=config.URL_PREFIX)
    logger.info("Server started 🚀")

    yield

    # cleanup on shutdown
    await Connections.close_connections()


app = FastAPI(lifespan=lifespan)
