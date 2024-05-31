from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    steps = relationship("Step", back_populates="recipe", cascade="all, delete-orphan")
    pastry = relationship("Pastry", uselist=False, back_populates="recipe")
