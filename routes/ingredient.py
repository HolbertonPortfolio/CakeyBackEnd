from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies.dependencies import get_db
from models.ingredient import Ingredient
from schemas.ingredient import Ingredient as IngredientSchema, IngredientCreate

router = APIRouter()


@router.post("/ingredients/", response_model=IngredientSchema)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = Ingredient(name=ingredient.name, description=ingredient.description)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.get("/ingredients/", response_model=List[IngredientSchema])
def read_ingredients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).offset(skip).limit(limit).all()
    return ingredients


@router.get("/ingredients/{ingredient_id}", response_model=IngredientSchema)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.put("/ingredients/{ingredient_id}", response_model=IngredientSchema)
def update_ingredient(ingredient_id: int, ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db_ingredient.name = ingredient.name
    db_ingredient.description = ingredient.description
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(db_ingredient)
    db.commit()
    return {"detail": "Ingredient deleted"}
