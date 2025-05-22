# app/models/cart.py

from pydantic import BaseModel, Field
from typing import List
from app.schemas.cart import CartItem

class CartModel(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItem] = []

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True