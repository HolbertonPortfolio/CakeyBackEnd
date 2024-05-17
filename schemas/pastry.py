from pydantic import BaseModel, HttpUrl, validator
from typing import Optional


class PastryBase(BaseModel):
    name: str
    description: str
    image_url: Optional[HttpUrl] = None

    @validator('name', 'description')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Must not be empty')
        return v


class PastryCreate(PastryBase):
    pass


class Pastry(PastryBase):
    id: int

    class Config:
        orm_mode = True
