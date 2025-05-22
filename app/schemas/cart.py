from pydantic import BaseModel, Field
from typing import List, Optional

class CartItem(BaseModel):
    product_id: str = Field(..., description="Product ID as string")
    quantity: int = Field(..., gt=0, example=1)

class CartCreate(BaseModel):
    items: List[CartItem] = []

class CartResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItem] = []

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True