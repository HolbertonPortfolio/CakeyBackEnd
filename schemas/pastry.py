from typing import List, Optional
from pydantic import BaseModel, HttpUrl, validator
from schemas.ingredient import Ingredient
from schemas.recipe import Recipe, RecipeCreate


class PastryBase(BaseModel):
    name: str
    description: str
    image_url: Optional[HttpUrl]

    @validator('name', 'description')
    def must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Must not be empty')
        return v


class PastryCreate(PastryBase):
    ingredients: Optional[List[int]]
    recipe: RecipeCreate


class Pastry(PastryBase):
    id: int
    ingredients: List[Ingredient]
    recipe: Recipe

    class Config:
        orm_mode = True


class PastryList(BaseModel):
    id: int
    name: str
    description: str
    image_url: Optional[HttpUrl]
