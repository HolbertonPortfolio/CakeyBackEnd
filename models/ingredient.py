from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    pastries = relationship('Pastry', secondary='pastry_ingredient', back_populates="ingredients")
