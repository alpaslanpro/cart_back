# app/repositories/cart.py

from typing import Optional
from app.db.mongo import get_db
from app.models.cart import CartModel
from app.schemas.cart import CartCreate, CartItem
from bson import ObjectId

CART_COLLECTION = "carts"

async def create_cart(cart_data: CartCreate) -> CartModel:
    db = get_db()
    cart_dict = cart_data.model_dump()
    result = await db[CART_COLLECTION].insert_one(cart_dict)
    cart = await db[CART_COLLECTION].find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for Pydantic model
    cart["_id"] = str(cart["_id"])
    
    return CartModel(**cart)

async def get_cart(cart_id: str) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if cart:
        # Convert ObjectId to string for Pydantic model
        cart["_id"] = str(cart["_id"])
        return CartModel(**cart)
    return None

async def add_item_to_cart(cart_id: str, item: CartItem) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    # Convert product_id to string for comparison
    product_id_str = str(item.product_id)
    
    # Upsert item quantity if product_id exists else push new item
    update_result = await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id), "items.product_id": product_id_str},
        {"$inc": {"items.$.quantity": item.quantity}}
    )
    if update_result.modified_count == 0:
        # item not found, add new
        item_dict = item.model_dump()
        item_dict["product_id"] = product_id_str  # Ensure it's stored as string
        await db[CART_COLLECTION].update_one(
            {"_id": ObjectId(cart_id)},
            {"$push": {"items": item_dict}}
        )
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        return CartModel(**updated_cart)
    return None

async def remove_item_from_cart(cart_id: str, product_id: str) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id)},
        {"$pull": {"items": {"product_id": product_id}}}
    )
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        return CartModel(**updated_cart)
    return None