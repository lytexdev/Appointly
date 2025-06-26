from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./appointly.db"
    
    # SMTP Configuration
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str = "Appointly"
    
    # Admin Configuration
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Configuration
    APP_NAME: str = "Appointly"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
