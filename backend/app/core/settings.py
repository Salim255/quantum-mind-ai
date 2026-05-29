from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    API_PREFIX: str = "/api/v1"

    GROAI_API_KEY: str

    ENV: str

    QDRANT_API_KEY: str
    
    QDRANT_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def is_dev(self):
        return self.ENV.lower() == "development"

@lru_cache
def get_settings() -> Settings:
    return Settings()
