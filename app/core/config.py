from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SUPABASE_URL: str
    SUPABASE_KEY: str

    DATABASE_URL: str

    CORS_ORIGINS: str


    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    SUPABASE_JWKS_URL: str

    FRONTEND_URL: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()