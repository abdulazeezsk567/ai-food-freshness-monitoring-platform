import os
from typing import List, Union, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

def normalize_database_url(url: str) -> str:
    """
    Normalizes database connection strings for SQLAlchemy compatibility.
    Specifically ensures PostgreSQL connections use the installed psycopg2 driver:
    - 'postgres://' -> 'postgresql+psycopg2://'
    - 'postgresql://' -> 'postgresql+psycopg2://'
    - 'postgresql+psycopg://' -> 'postgresql+psycopg2://'
    - 'postgresql+psycopg2://' -> unchanged
    Other database schemes (such as 'sqlite://') are preserved as-is.
    """
    if not url:
        return url

    url = url.strip().strip("'\"")
    if url.startswith("postgresql+psycopg2://"):
        return url
    if url.startswith("postgresql+psycopg://"):
        return "postgresql+psycopg2://" + url[len("postgresql+psycopg://"):]
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        extra="ignore"
    )

    APP_NAME: str = "Food Freshness Monitoring Platform"
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "super_secret_jwt_key_change_in_production_32bytes_min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ADMIN_EMAIL: str = "admin@foodfreshness.com"
    ADMIN_PASSWORD: str = "Admin123!"
    
    # Database URL
    DATABASE_URL: str = "sqlite:///./food_freshness.db"

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def assemble_database_url(cls, v: str) -> str:
        return normalize_database_url(v)
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]
    CORS_ORIGIN_REGEX: Optional[str] = r"^https:\/\/.*\.onrender\.com$"

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # Uploads Storage
    UPLOAD_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))

settings = Settings()
