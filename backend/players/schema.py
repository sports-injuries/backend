from pydantic import BaseModel


class PlayerSchema(BaseModel):
    uid: int
    name: str
    description: str
