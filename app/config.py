from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

Environment = Literal["local", "test", "dev", "stg", "prd"]


class BasesConfig(BaseSettings):
    ENVIRONMENT: Environment = Field(
        description="Environment process is running in", default="local"
    )


config = BasesConfig()
