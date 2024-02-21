from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    GRPC_PORT: Optional[str] = None
    MILVUS_URL: Optional[str] = None
    LUNA_SERVICE_URL: Optional[str] = None


settings = Settings()
