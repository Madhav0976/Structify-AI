"""
Structify AI - Application Configuration

Loads environment variables from .env file using Pydantic Settings.
This gives us:
  - Type validation (PORT must be an int, DEBUG must be a bool)
  - Default values (if a variable is missing from .env)
  - Centralized access (import settings anywhere)
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- App Info ---
    APP_NAME: str = "Structify AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./structify.db"

    # --- CORS ---
    # Origins allowed to access our API (frontend URLs)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",     # Next.js dev server
        "http://127.0.0.1:3000",
        "http://localhost:8000",     # FastAPI docs
        "https://structify-ai-beta.vercel.app",
    ]

    # --- Feature Flags (A/B Testing) ---
    ENABLE_OCR_REPAIR: bool = True   # Toggle the NLP Error Repair Pipeline

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single settings instance to use across the app
settings = Settings()
