from typing import List
from pydantic import BaseModel, HttpUrl, validator
from schemas.ingredient import Ingredient


class PastryBase(BaseModel):
    name: str
    description: str
    image_url: HttpUrl = None

    @validator('name', 'description')
    def must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Must not be empty')
        return v


class PastryCreate(PastryBase):
    ingredients: List[int] = []


class Pastry(PastryBase):
    id: int
    ingredients: List[Ingredient] = []

    class Config:
        orm_mode = True
