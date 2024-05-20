from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies.dependencies import get_db
from models.pastry import Pastry
from models.ingredient import Ingredient
from schemas.pastry import Pastry as PastrySchema, PastryCreate

router = APIRouter()


@router.post("/pastries/", response_model=PastrySchema)
def create_pastry(pastry: PastryCreate, db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).filter(Ingredient.id.in_(pastry.ingredients)).all()
    db_pastry = Pastry(
        name=pastry.name,
        description=pastry.description,
        image_url=pastry.image_url,
        ingredients=ingredients
    )
    db.add(db_pastry)
    db.commit()
    db.refresh(db_pastry)
    return db_pastry


@router.get("/pastries/", response_model=List[PastrySchema])
def read_pastries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pastries = db.query(Pastry).offset(skip).limit(limit).all()
    return pastries


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
