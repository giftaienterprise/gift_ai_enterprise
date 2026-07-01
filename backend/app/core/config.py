from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Gift AI Enterprise"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    UPLOAD_DIR: str = "uploads"
    UPLOAD_URL_PREFIX: str = "/uploads"

    DEEPSEEK_API_KEY: str | None = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    AI_CACHE_TTL_SECONDS: int = 86400
    AI_CACHE_PROMPT_VERSION: str = "v1"
    AI_CACHE_MODEL_VERSION: str = "deepseek-v1"
    AI_CACHE_ENABLED: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()