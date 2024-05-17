from sqlalchemy import Column, Integer, String
from config.db import Base


class Pastry(Base):
    __tablename__ = "pastries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    image_url = Column(String(255))
