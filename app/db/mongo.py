# app/db/mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

mongo_client = None
_db = None  # use underscore to indicate internal

async def connect_to_mongo():
    global mongo_client, _db
    try:
        mongo_client = AsyncIOMotorClient(settings.mongo_uri)
        _db = mongo_client[settings.mongo_db]
        # Test the connection
        await _db.command("ping")
        logging.info(f"Connected to MongoDB database: {settings.mongo_db}")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise

def get_db():
    if _db is None:
        raise Exception("Database not connected. Call connect_to_mongo() first.")
    return _db

async def close_mongo_connection():
    global mongo_client, _db
    if mongo_client:
        mongo_client.close()
        _db = None
        logging.info("Disconnected from MongoDB")