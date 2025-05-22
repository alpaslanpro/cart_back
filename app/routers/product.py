# app/routers/product.py

from fastapi import APIRouter, HTTPException, Response, status
from app.schemas.product import ProductCreate, ProductResponse
from app.repositories.product import create_product, get_all_products, get_product_by_id, delete_product
from typing import List

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_new_product(product: ProductCreate):
    """POST /api/v1/products - Создать новый продукт"""
    new_product = await create_product(product)
    if not new_product:
        raise HTTPException(status_code=400, detail="Failed to create product")
    return new_product

@router.get("/", response_model=List[ProductResponse])
async def list_all_products():
    """GET /api/v1/products - Получить список всех продуктов"""
    products = await get_all_products()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """GET /api/v1/products/{productId} - Получить продукт по ID"""
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: str):
    """DELETE /api/v1/products/{productId} - Удалить продукт"""
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)