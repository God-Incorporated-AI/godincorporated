"""
Configuration management for God Incorporated.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    environment: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "God Incorporated Oracle API"
    api_version: str = "1.0.0"
    api_description: str = "An AI-powered oracle platform exploring wisdom, inquiry, and value-for-value interaction"
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    
    # Database Configuration
    database_url: str = "sqlite:///./godincorporated.db"
    
    # Value-for-Value Configuration
    enable_payments: bool = False
    payment_provider: str = "stripe"
    payment_api_key: str = ""
    
    # Voice Configuration
    enable_voice: bool = True
    voice_rate: int = 150
    voice_volume: float = 1.0
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
