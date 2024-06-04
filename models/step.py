from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from config.db import Base


class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    timer = Column(Integer, nullable=False)
    step_number = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship("Recipe", back_populates="steps")
