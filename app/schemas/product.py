# app/schemas/product.py

from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., example="iPhone 15")
    description: Optional[str] = Field(None, example="Latest Apple smartphone")
    price: float = Field(..., gt=0, example=1299.99)
    in_stock: int = Field(..., ge=0, example=10)

class ProductResponse(ProductCreate):
    id: str = Field(..., example="665dd299f2f5b3f3e99f8ef4")