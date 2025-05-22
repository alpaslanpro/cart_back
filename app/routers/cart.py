# app/routers/cart.py

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.schemas.cart import CartCreate, CartResponse, CartItem, ItemUpdate, CheckoutResponse
from app.repositories.cart import (
    create_cart, get_cart, get_all_carts, add_item_to_cart_or_create,
    update_item_quantity, remove_item_from_cart, clear_cart, checkout_cart
)
from typing import List

router = APIRouter()

@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def create_new_cart(cart: CartCreate, response: Response):
    """POST /api/v1/carts - Создать новую корзину"""
    new_cart = await create_cart(cart)
    if not new_cart:
        raise HTTPException(status_code=400, detail="Failed to create cart")
    
    # Add Location header with cart URL
    response.headers["Location"] = f"/api/v1/carts/{new_cart.id}"
    return new_cart

@router.get("/", response_model=List[CartResponse])
async def get_all_carts_endpoint():
    """GET /api/v1/carts - Получить список всех корзин (административный)"""
    carts = await get_all_carts()
    return carts

@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart_by_id(cart_id: str):
    """GET /api/v1/carts/{cartId} - Получить содержимое конкретной корзины"""
    cart = await get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/{cart_id}/items", response_model=CartResponse)
async def add_item_to_cart_endpoint(cart_id: str, item: CartItem):
    """POST /api/v1/carts/{cartId}/items - Добавить товар в корзину"""
    updated_cart = await add_item_to_cart_or_create(cart_id, item)
    if not updated_cart:
        raise HTTPException(status_code=400, detail="Failed to add item to cart")
    return updated_cart

@router.put("/{cart_id}/items/{item_id}", response_model=CartResponse)
async def update_cart_item(cart_id: str, item_id: str, item_update: ItemUpdate):
    """PUT /api/v1/carts/{cartId}/items/{itemId} - Обновить количество товара"""
    updated_cart = await update_item_quantity(cart_id, item_id, item_update.quantity)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart or item not found")
    return updated_cart

@router.delete("/{cart_id}/items/{item_id}", response_model=CartResponse)
async def remove_item_from_cart_endpoint(cart_id: str, item_id: str):
    """DELETE /api/v1/carts/{cartId}/items/{itemId} - Удалить товар из корзины"""
    updated_cart = await remove_item_from_cart(cart_id, item_id)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart or item not found")
    return updated_cart

@router.delete("/{cart_id}", response_model=CartResponse)
async def clear_cart_endpoint(cart_id: str):
    """DELETE /api/v1/carts/{cartId} - Очистить корзину"""
    cleared_cart = await clear_cart(cart_id)
    if not cleared_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cleared_cart

@router.post("/{cart_id}/checkout", response_model=CheckoutResponse)
async def checkout_cart_endpoint(cart_id: str):
    """POST /api/v1/carts/{cartId}/checkout - Оформить заказ"""
    order_summary = await checkout_cart(cart_id)
    if not order_summary:
        raise HTTPException(status_code=404, detail="Cart not found")
    return order_summary