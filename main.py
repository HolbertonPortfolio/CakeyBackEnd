from fastapi import FastAPI
from config.db import Base, engine
from routes.pastry import router as pastry_router
from routes.ingredient import router as ingredient_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(pastry_router, prefix="/api", tags=["pastries"])
app.include_router(ingredient_router, prefix="/api", tags=["ingredients"])
