from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    GROAI_API_KEY: str
    

    model_config = SettingsConfigDict(env_file=".env")