from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Gift AI Enterprise"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./gift_ai.db"

    SECRET_KEY: str = "GiftAI2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()