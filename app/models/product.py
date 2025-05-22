# app/models/product.py

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from app.utils.pyobjectid import PyObjectId

class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
