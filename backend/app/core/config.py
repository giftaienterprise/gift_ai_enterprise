from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Gift AI Enterprise"
    APP_VERSION: str = "2.0.0"

    DEBUG: bool = True

    DATABASE_URL: str = "mysql+pymysql://root:123456@127.0.0.1:3306/gift_ai_enterprise"

    SECRET_KEY: str = "gift-ai-enterprise-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    OPENAI_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    UPLOAD_DIR: str = "../uploads"
    UPLOAD_URL_PREFIX: str = "/uploads"

    STORAGE_DRIVER: str = "local"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()