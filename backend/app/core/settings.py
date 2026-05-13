from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")