from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_
from dependencies.dependencies import get_db
from models.pastry import Pastry
from models.ingredient import Ingredient
from schemas.pastry import Pastry as PastrySchema, PastryCreate, IngredientList

router = APIRouter()


@router.post("/pastries/", response_model=PastrySchema)
def create_pastry(pastry: PastryCreate, db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).filter(Ingredient.id.in_(pastry.ingredients)).all()
    if len(ingredients) != len(pastry.ingredients):
        raise HTTPException(status_code=400, detail="One or more ingredients not found")
    db_pastry = Pastry(
        name=pastry.name,
        description=pastry.description,
        image_url=pastry.image_url,
        ingredients=ingredients,
        recipe=pastry.recipe.dict() if pastry.recipe else None
    )
    db.add(db_pastry)
    db.commit()
    db.refresh(db_pastry)
    return db_pastry


@router.get("/pastries/")
def read_pastries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pastries = db.query(Pastry).offset(skip).limit(limit).all()
    results = []
    for pastry in pastries:
        result = {'id': pastry.id, 'name': pastry.name, 'description': pastry.description,
                  'image_url': pastry.image_url}
        results.append(result)
    return results


@router.get("/pastries/{pastry_id}", response_model=PastrySchema)
def read_pastry(pastry_id: int, db: Session = Depends(get_db)):
    pastry = db.query(Pastry).filter(Pastry.id == pastry_id).first()
    if pastry is None:
        raise HTTPException(status_code=404, detail="Pastry not found")
    return pastry


@router.put("/pastries/{pastry_id}", response_model=PastrySchema)
def update_pastry(pastry_id: int, pastry: PastryCreate, db: Session = Depends(get_db)):
    db_pastry = db.query(Pastry).filter(Pastry.id == pastry_id).first()
    if db_pastry is None:
        raise HTTPException(status_code=404, detail="Pastry not found")
    if pastry.name is not None:
        db_pastry.name = pastry.name
    if pastry.description is not None:
        db_pastry.description = pastry.description
    if pastry.image_url is not None:
        db_pastry.image_url = pastry.image_url
    if pastry.ingredients or pastry.ingredients == []:
        ingredients = db.query(Ingredient).filter(Ingredient.id.in_(pastry.ingredients)).all()
        db_pastry.ingredients = ingredients

    db.commit()
    db.refresh(db_pastry)
    return db_pastry


@router.delete("/pastries/{pastry_id}")
def delete_pastry(pastry_id: int, db: Session = Depends(get_db)):
    db_pastry = db.query(Pastry).filter(Pastry.id == pastry_id).first()
    if db_pastry is None:
        raise HTTPException(status_code=404, detail="Pastry not found")
    db.delete(db_pastry)
    db.commit()
    return {"detail": "Pastry deleted"}


@router.post("/pastries/by-ingredients", response_model=List[PastrySchema])
def get_pastries_by_ingredients(ingredient_list: IngredientList, db: Session = Depends(get_db)):
    # Get the list of ingredient IDs
    ingredient_ids = ingredient_list.ingredients

    # Get pastries that contain any of the specified ingredients
    pastries = db.query(Pastry).join(Pastry.ingredients).filter(Ingredient.id.in_(ingredient_ids)).all()

    # Filter pastries to only include those that contain all the specified ingredients
    result = []
    for pastry in pastries:
        pastry_ingredient_ids = {ingredient.id for ingredient in pastry.ingredients}
        if all(ingredient_id in pastry_ingredient_ids for ingredient_id in ingredient_ids):
            result.append(pastry)

    return result


@router.get("/pastries/search/")
def search_pastries(query: str, db: Session = Depends(get_db)):
    pastries = db.query(Pastry).join(Pastry.ingredients).filter(
        or_(
            Pastry.name.ilike(f"{query}%"),
            # Pastry.description.ilike(f"%{query}%"),
            # Ingredient.name.ilike(f"%{query}%")
        )
    ).all()
    results = []
    for pastry in pastries:
        result = {'id': pastry.id, 'name': pastry.name, 'description': pastry.description,
                  'image_url': pastry.image_url}
        results.append(result)
    return results
