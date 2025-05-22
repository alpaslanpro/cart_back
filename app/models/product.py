# app/models/product.py

from pydantic import BaseModel, Field
from typing import Optional

class ProductModel(BaseModel):
    id: str = Field(..., alias="_id", description="Product ID as string")
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True