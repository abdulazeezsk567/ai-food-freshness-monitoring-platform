import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Food Freshness Monitoring Platform"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_jwt_key_change_in_production_32bytes_min")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./food_freshness.db"
    )
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
