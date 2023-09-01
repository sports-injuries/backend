from pydantic import BaseModel


class TeamSchema(BaseModel):
    uid: int
    name: str
    description: str
