"""
Application Configuration
Maps to: Problem Understanding - Define target audience and required inputs/outputs
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache
from pydantic import Field, computed_field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Application
    app_name: str = "Messaging API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./messaging.db"
    
    # JWT Authentication
    secret_key: str = "dev-secret-key-CHANGE-IN-PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS - Store as string internally
    allowed_origins_str: str = Field(default="http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:5501,http://127.0.0.1:5501,file://", alias="allowed_origins")
    
    @computed_field
    @property
    def allowed_origins(self) -> List[str]:
        """Parse comma-separated origins string to list"""
        return [origin.strip() for origin in self.allowed_origins_str.split(',') if origin.strip()]
    
    # Logging
    log_level: str = "INFO"
    
    # SendGrid Email Service
    sendgrid_api_key: str = "your-sendgrid-api-key-here"
    sendgrid_from_email: str = "noreply@messaging-api.com"
    
    # Email Notifications
    enable_email_notifications: bool = True
    app_url: str = "http://localhost:8000"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
