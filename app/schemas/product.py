# app/schemas/product.py

from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., example="iPhone 15")
    description: Optional[str] = Field(None, example="Latest Apple smartphone")
    price: float = Field(..., gt=0, example=1299.99)
    in_stock: int = Field(..., ge=0, example=10)

class ProductResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Product ID as string")
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True