from sqlalchemy import Column, Integer, String, Table, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config.db import Base

# Association table
pastry_ingredient_association = Table(
    'pastry_ingredient',
    Base.metadata,
    Column('pastry_id', Integer, ForeignKey('pastries.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)


class Pastry(Base):
    __tablename__ = "pastries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    image_url = Column(String(255))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    recipe = relationship("Recipe", back_populates="pastry")
    ingredients = relationship('Ingredient', secondary='pastry_ingredient', back_populates="pastries")
