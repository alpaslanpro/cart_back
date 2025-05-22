# app/routers/cart.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_cart():
    return {"message": "Cart endpoint working"}
