from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

mongo_client = None
db = None

async def connect_to_mongo():
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    db = mongo_client[settings.mongo_db]
    
async def close_mongo_connection():
    global mongo_client
    mongo_client.close()