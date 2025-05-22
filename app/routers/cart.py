# app/routers/cart.py

from fastapi import APIRouter, HTTPException
from app.schemas.cart import CartCreate, CartResponse, CartItem
from app.repositories.cart import create_cart, get_cart, add_item_to_cart, remove_item_from_cart
from typing import List

router = APIRouter()

@router.post("/", response_model=CartResponse)
async def create_new_cart(cart: CartCreate):
    new_cart = await create_cart(cart)
    if not new_cart:
        raise HTTPException(status_code=400, detail="Failed to create cart")
    return new_cart

@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart_by_id(cart_id: str):
    cart = await get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/{cart_id}/items", response_model=CartResponse)
async def add_item(cart_id: str, item: CartItem):
    updated_cart = await add_item_to_cart(cart_id, item)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart or Product not found")
    return updated_cart

@router.delete("/{cart_id}/items/{product_id}", response_model=CartResponse)
async def remove_item(cart_id: str, product_id: str):
    updated_cart = await remove_item_from_cart(cart_id, product_id)
    if not updated_cart:
        raise HTTPException(status_code=404, detail="Cart or Product not found")
    return updated_cart

