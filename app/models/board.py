from pydantic import BaseModel


class Board(BaseModel):
    name: str
