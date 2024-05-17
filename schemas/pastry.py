from pydantic import BaseModel


class PastryBase(BaseModel):
    name: str


class PastryCreate(PastryBase):
    pass


class Pastry(PastryBase):
    id: int

    class Config:
        orm_mode = True
