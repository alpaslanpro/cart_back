# app/models/cart.py

from pydantic import BaseModel, Field
from typing import List
from app.schemas.cart import CartItemWithDetails

class CartModel(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItemWithDetails] = []
    total_amount: float = Field(..., description="Total cart value")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True