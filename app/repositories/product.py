# app/repositories/product.py

from typing import List, Optional
from app.db.mongo import db
from app.schemas.product import ProductCreate
from app.models.product import ProductModel
from bson import ObjectId

PRODUCT_COLLECTION = "products"

async def create_product(product_data: ProductCreate) -> ProductModel:
    product_dict = product_data.model_dump()
    result = await db[PRODUCT_COLLECTION].insert_one(product_dict)
    product = await db[PRODUCT_COLLECTION].find_one({"_id": result.inserted_id})
    return ProductModel(**product)

async def get_product_by_id(product_id: str) -> Optional[ProductModel]:
    if not ObjectId.is_valid(product_id):
        return None
    product = await db[PRODUCT_COLLECTION].find_one({"_id": ObjectId(product_id)})
    if product:
        return ProductModel(**product)
    return None

async def get_all_products() -> List[ProductModel]:
    products_cursor = db[PRODUCT_COLLECTION].find()
    products = []
    async for product in products_cursor:
        products.append(ProductModel(**product))
    return products


