from pydantic import BaseModel


class InjurySchema(BaseModel):
    uid: int
    name: str
    description: str
