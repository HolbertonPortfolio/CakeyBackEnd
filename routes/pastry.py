from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies.dependencies import get_db  # Updated import
from models.pastry import Pastry
from schemas.pastry import Pastry as PastrySchema, PastryCreate

router = APIRouter()


@router.post("/pastries/", response_model=PastrySchema)
def create_pastry(pastry: PastryCreate, db: Session = Depends(get_db)):
    db_pastry = Pastry(name=pastry.name)
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
    db_pastry.name = pastry.name
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
