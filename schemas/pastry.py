from pydantic import BaseModel, validator


class PastryBase(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v


class PastryCreate(PastryBase):
    pass


class Pastry(PastryBase):
    id: int

    class Config:
        orm_mode = True
