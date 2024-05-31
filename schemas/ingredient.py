from typing import Optional, List

from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    description: Optional[str] = None


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class IngredientList(BaseModel):
    ingredients: List[int]
