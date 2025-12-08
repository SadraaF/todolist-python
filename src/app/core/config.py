"""Application configuration management.

This module uses Pydantic's BaseSettings to load and validate application
settings from environment variables and .env files.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    MAX_NUMBER_OF_PROJECT: int = 10
    MAX_NUMBER_OF_TASK: int = 20

    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        """Construct the asynchronous database connection URL.

        :return: The full database connection string.
        """
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        """Pydantic model configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    """Return the application settings instance.

    Uses lru_cache to ensure settings are loaded only once.

    :return: A singleton Settings instance.
    """
    return Settings()