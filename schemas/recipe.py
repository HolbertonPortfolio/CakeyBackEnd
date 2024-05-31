from typing import List
from pydantic import BaseModel, validator
from schemas.step import StepCreate, Step


class RecipeBase(BaseModel):
    name: str
    steps: List[StepCreate]

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    steps: List[Step]

    class Config:
        orm_mode = True
