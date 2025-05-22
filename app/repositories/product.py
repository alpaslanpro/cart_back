# app/repositories/product.py

from typing import List, Optional
from app.db.mongo import get_db
from app.schemas.product import ProductCreate
from app.models.product import ProductModel
from bson import ObjectId

PRODUCT_COLLECTION = "products"

async def create_product(product_data: ProductCreate) -> ProductModel:
    """Create a new product"""
    db = get_db()
    product_dict = product_data.model_dump()
    result = await db[PRODUCT_COLLECTION].insert_one(product_dict)
    product = await db[PRODUCT_COLLECTION].find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for Pydantic model
    product["_id"] = str(product["_id"])
    
    return ProductModel(**product)

async def get_product_by_id(product_id: str) -> Optional[ProductModel]:
    """Get product by ID"""
    if not ObjectId.is_valid(product_id):
        return None
    db = get_db()
    product = await db[PRODUCT_COLLECTION].find_one({"_id": ObjectId(product_id)})
    if product:
        # Convert ObjectId to string for Pydantic model
        product["_id"] = str(product["_id"])
        return ProductModel(**product)
    return None

async def get_all_products() -> List[ProductModel]:
    """Get all products"""
    db = get_db()
    products_cursor = db[PRODUCT_COLLECTION].find()
    products = []
    async for product in products_cursor:
        # Convert ObjectId to string for Pydantic model
        product["_id"] = str(product["_id"])
        products.append(ProductModel(**product))
    return products

async def delete_product(product_id: str) -> bool:
    """Delete product by ID"""
    if not ObjectId.is_valid(product_id):
        return False
    db = get_db()
    result = await db[PRODUCT_COLLECTION].delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0