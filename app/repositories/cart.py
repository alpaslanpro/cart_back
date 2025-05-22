# app/repositories/cart.py

from typing import List, Optional
from app.db.mongo import get_db
from app.models.cart import CartModel
from app.schemas.cart import CartCreate, CartItem, CartItemWithDetails
from bson import ObjectId

CART_COLLECTION = "carts"
PRODUCT_COLLECTION = "products"

async def get_product_details(product_id: str) -> Optional[dict]:
    """Get product details by ID"""
    if not ObjectId.is_valid(product_id):
        return None
    db = get_db()
    product = await db[PRODUCT_COLLECTION].find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
    return product

async def enrich_cart_items(items: List[dict]) -> tuple[List[CartItemWithDetails], float]:
    """Enrich cart items with product details and calculate total"""
    enriched_items = []
    total_amount = 0.0
    
    for item in items:
        product = await get_product_details(item["product_id"])
        if product:
            item_total = product["price"] * item["quantity"]
            enriched_item = CartItemWithDetails(
                product_id=item["product_id"],
                product_name=product["name"],
                quantity=item["quantity"],
                price=product["price"],
                total_price=item_total
            )
            enriched_items.append(enriched_item)
            total_amount += item_total
        else:
            # Product not found, include item with minimal info
            enriched_item = CartItemWithDetails(
                product_id=item["product_id"],
                product_name="Product Not Found",
                quantity=item["quantity"],
                price=0.0,
                total_price=0.0
            )
            enriched_items.append(enriched_item)
    
    return enriched_items, total_amount

async def create_cart(cart_data: CartCreate) -> CartModel:
    db = get_db()
    cart_dict = cart_data.model_dump()
    result = await db[CART_COLLECTION].insert_one(cart_dict)
    cart = await db[CART_COLLECTION].find_one({"_id": result.inserted_id})
    
    # Convert ObjectId to string for Pydantic model
    cart["_id"] = str(cart["_id"])
    
    # Enrich items with product details and calculate total
    enriched_items, total_amount = await enrich_cart_items(cart.get("items", []))
    
    return CartModel(
        id=cart["_id"],
        items=enriched_items,
        total_amount=total_amount
    )

async def get_cart(cart_id: str) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if cart:
        # Convert ObjectId to string for Pydantic model
        cart["_id"] = str(cart["_id"])
        
        # Enrich items with product details and calculate total
        enriched_items, total_amount = await enrich_cart_items(cart.get("items", []))
        
        return CartModel(
            id=cart["_id"],
            items=enriched_items,
            total_amount=total_amount
        )
    return None

async def get_all_carts() -> List[CartModel]:
    db = get_db()
    carts_cursor = db[CART_COLLECTION].find()
    carts = []
    async for cart in carts_cursor:
        # Convert ObjectId to string for Pydantic model
        cart["_id"] = str(cart["_id"])
        
        # Enrich items with product details and calculate total
        enriched_items, total_amount = await enrich_cart_items(cart.get("items", []))
        
        cart_model = CartModel(
            id=cart["_id"],
            items=enriched_items,
            total_amount=total_amount
        )
        carts.append(cart_model)
    return carts

async def add_item_to_cart(cart_id: str, item: CartItem) -> Optional[CartModel]:
    if not ObjectId.is_valid(cart_id):
        return None
    
    # Verify product exists
    product = await get_product_details(item.product_id)
    if not product:
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
        
        # Enrich items with product details and calculate total
        enriched_items, total_amount = await enrich_cart_items(updated_cart.get("items", []))
        
        return CartModel(
            id=updated_cart["_id"],
            items=enriched_items,
            total_amount=total_amount
        )
    return None

async def add_item_to_cart_or_create(cart_id: str, item: CartItem) -> CartModel:
    """Add item to cart, create cart if it doesn't exist"""
    db = get_db()
    
    # Verify product exists
    product = await get_product_details(item.product_id)
    if not product:
        raise ValueError(f"Product {item.product_id} not found")
    
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
        
        # Enrich items with product details and calculate total
        enriched_items, total_amount = await enrich_cart_items(updated_cart.get("items", []))
        
        return CartModel(
            id=updated_cart["_id"],
            items=enriched_items,
            total_amount=total_amount
        )
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
        
        # Enrich items with product details and calculate total
        enriched_items, total_amount = await enrich_cart_items(updated_cart.get("items", []))
        
        return CartModel(
            id=updated_cart["_id"],
            items=enriched_items,
            total_amount=total_amount
        )
    return None

async def clear_cart(cart_id: str) -> Optional[CartModel]:
    """Clear all items from cart but keep the cart"""
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    result = await db[CART_COLLECTION].update_one(
        {"_id": ObjectId(cart_id)},
        {"$set": {"items": []}}
    )
    if result.matched_count == 0:
        return None
    
    updated_cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if updated_cart:
        # Convert ObjectId to string for Pydantic model
        updated_cart["_id"] = str(updated_cart["_id"])
        
        return CartModel(
            id=updated_cart["_id"],
            items=[],
            total_amount=0.0
        )
    return None

async def delete_cart(cart_id: str) -> bool:
    """Delete cart completely"""
    if not ObjectId.is_valid(cart_id):
        return False
    db = get_db()
    result = await db[CART_COLLECTION].delete_one({"_id": ObjectId(cart_id)})
    return result.deleted_count > 0

async def checkout_cart(cart_id: str) -> Optional[dict]:
    """Process cart checkout - returns order summary and deletes the cart"""
    if not ObjectId.is_valid(cart_id):
        return None
    db = get_db()
    cart = await db[CART_COLLECTION].find_one({"_id": ObjectId(cart_id)})
    if not cart:
        return None
    
    # Enrich items and calculate total
    enriched_items, total_amount = await enrich_cart_items(cart.get("items", []))
    
    # Create order summary
    order_summary = {
        "cart_id": str(cart["_id"]),
        "items": [item.model_dump() for item in enriched_items],
        "total_amount": total_amount,
        "status": "processed"
    }
    
    # Delete cart after checkout
    await delete_cart(cart_id)
    
    return order_summary