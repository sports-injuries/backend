from pydantic import BaseModel


class PlayerSchema(BaseModel):
    uid: int
    name: str
    description: str
    team_id: int

    class Config:
        orm_mode = True
