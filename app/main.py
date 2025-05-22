# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.routers import cart, product

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Korzina Cart API", 
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Products"])

@app.get("/")
async def root():
    return {"message": "Korzina Cart API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}