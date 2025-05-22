# app/models/cart.py

from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.cart import CartItem

class CartModel(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItem] = []
    total_amount: Optional[float] = Field(default=0, description="Total cart value")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True