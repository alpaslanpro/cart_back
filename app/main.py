# app/main.py


from fastapi import FastAPI
from app.core.config import settings
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.routers import cart, product



app = FastAPI(title="Korzina Cart API", version="0.1.0")

app.include_router(cart.router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Products"])

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()