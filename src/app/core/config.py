import os
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
        """Construct the database connection URL."""
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    """Returns the settings instance, cached for performance."""
    return Settings()