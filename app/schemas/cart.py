from pydantic import BaseModel, Field
from typing import List, Optional

class CartItem(BaseModel):
    product_id: str = Field(..., description="Product ID as string", alias="productId")
    quantity: int = Field(..., gt=0, example=1)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class CartItemWithDetails(BaseModel):
    product_id: str = Field(..., description="Product ID as string")
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., gt=0, example=1)
    price: float = Field(..., description="Unit price")
    total_price: float = Field(..., description="Total price for this item")

class CartCreate(BaseModel):
    items: List[CartItem] = []

class CartResponse(BaseModel):
    id: str = Field(..., alias="_id", description="Cart ID as string")
    items: List[CartItemWithDetails] = []
    total_amount: float = Field(..., description="Total cart value")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, example=1)

class CheckoutResponse(BaseModel):
    cart_id: str = Field(..., description="Cart ID")
    items: List[CartItemWithDetails] = Field(..., description="Cart items with details")
    total_amount: float = Field(..., description="Total order amount")
    status: str = Field(..., description="Order status")