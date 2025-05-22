# app/routers/product.py

from fastapi import APIRouter, HTTPException
from app.schemas.product import ProductCreate, ProductResponse
from app.repositories.product import create_product, get_all_products, get_product_by_id
from typing import List

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def create_new_product(product: ProductCreate):
    new_product = await create_product(product)
    if not new_product:
        raise HTTPException(status_code=400, detail="Failed to create product")
    return new_product

@router.get("/", response_model=List[ProductResponse])
async def list_all_products():
    products = await get_all_products()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product