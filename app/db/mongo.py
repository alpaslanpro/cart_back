# app/db/mongo.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

mongo_client = None
_db = None  # use underscore to indicate internal

async def connect_to_mongo():
    global mongo_client, _db
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    _db = mongo_client[settings.mongo_db]

def get_db():
    if _db is None:
        raise Exception("Database not connected")
    return _db

async def close_mongo_connection():
    global mongo_client
    if mongo_client:
        mongo_client.close()