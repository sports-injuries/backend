from pydantic import BaseModel


class Team(BaseModel):
    uid: int | None
    name: str
    description: str
