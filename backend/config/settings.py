from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./appointly.db"
    
    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    SMTP_FROM_EMAIL: str = "your-email@gmail.com"
    SMTP_FROM_NAME: str = "Appointly"
    
    # Admin Configuration
    ADMIN_EMAIL: str = "admin@appointly.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-make-it-long-and-random-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App Configuration
    APP_NAME: str = "Appointly"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
