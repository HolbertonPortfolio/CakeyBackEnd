from fastapi import FastAPI
from config.db import Base, engine
from routes.pastry import router as pastry_router

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(pastry_router, prefix="/api", tags=["pastries"])
