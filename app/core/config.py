# app/core/config.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "cartdb")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
settings = Settings()