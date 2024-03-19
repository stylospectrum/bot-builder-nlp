from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PORT: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    MILVUS_URL: Optional[str] = None
    LUNA_SERVICE_URL: Optional[str] = None
    BOT_BUILDER_STORY_SERVICE_URL: Optional[str] = None
    BOT_BUILDER_ENTITY_SERVICE_URL: Optional[str] = None


settings = Settings()
