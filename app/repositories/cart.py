# app/repositories/cart.py

from typing import List, Optional
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

async def get_all_carts() -> List[CartModel]:
    db = get_db()
    carts_cursor = db[CART_COLLECTION].find()
    carts = []
    async for cart in carts_cursor:
        # Convert ObjectId to string for Pydantic model
        cart["_id"] = str(cart["_id"])
        carts.append(CartModel(**cart))
    return carts

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

async def add_item_to_cart_or_create(cart_id: str, item: CartItem) -> CartModel:
    """Add item to cart, create cart if it doesn't exist"""
    db = get_db()
    
    if ObjectId.is_valid(cart_id):
        # Try to add to existing cart
        existing_cart = await add_item_to_cart(cart_id, item)
        if existing_cart:
            return existing_cart
    
    # Cart doesn't exist, create new one
    cart_data = CartCreate(items=[item])
    return await create_cart(cart_data)

async def update_item_quantity(cart_id: str, item_id: str, quantity: int) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    
    # Update the quantity of specific item
    await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id), "items.product_id": item_id},
        {"$set": {"items.$.quantity": quantity}}
    )
    
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        return CartModel(**updated_cart)
    return None

async def remove_item_from_cart(cart_id: str, item_id: str) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id)},
        {"$pull": {"items": {"product_id": item_id}}}
    )
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        return CartModel(**updated_cart)
    return None

async def clear_cart(cart_id: str) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id)},
        {"$set": {"items": []}}
    )
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        return CartModel(**updated_cart)
    return None

async def checkout_cart(cart_id: str) -> Optional[dict]:
    """Process cart checkout - returns order summary"""
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if not cart:
        return None
    
    # Calculate total
    total = 0
    for item in cart.get("items", []):
        # In real implementation, you'd fetch product price from products collection
        # For now, assuming items have price field or default price
        item_price = item.get("price", 0)  # This should come from product lookup
        total += item_price * item.get("quantity", 0)
    
    # Create order summary
    order_summary = {
        "cart_id": str(cart["_id"]),
        "items": cart.get("items", []),
        "total_amount": total,
        "status": "processed"
    }
    
    # Optionally clear cart after checkout
    await clear_cart(cart_id)
    
    return order_summary