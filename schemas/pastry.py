from typing import List, Optional
from pydantic import BaseModel, HttpUrl, validator
from schemas.ingredient import Ingredient


class Recipe(BaseModel):
    steps: List[str]
    timers: List[int]

    @validator('steps')
    def steps_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Steps must not be empty')
        return v

    @validator('timers')
    def timers_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Timers must not be empty')
        return v


class PastryBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    image_url: Optional[HttpUrl]
    recipe: Optional[Recipe] = None

    @validator('name', 'description')
    def must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Must not be empty')
        return v


class PastryCreate(PastryBase):
    ingredients: Optional[List[int]]


class Pastry(PastryBase):
    id: int
    ingredients: List[Ingredient]

    class Config:
        orm_mode = True
