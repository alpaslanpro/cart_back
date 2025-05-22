from pydantic import BaseModel, Field
from typing import List, Optional

class CartItem(BaseModel):
    product_id: str = Field(..., description="Product ID as string", alias="productId")
    quantity: int = Field(..., gt=0, example=1)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class CartCreate(BaseModel):
    items: List[CartItem] = []

class CartResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItem] = []
    total_amount: Optional[float] = Field(default=0, description="Total cart value")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, example=1)

class CheckoutResponse(BaseModel):
    cart_id: str = Field(..., description="Cart ID")
    items: List[dict] = Field(..., description="Cart items")
    total_amount: float = Field(..., description="Total order amount")
    status: str = Field(..., description="Order status")