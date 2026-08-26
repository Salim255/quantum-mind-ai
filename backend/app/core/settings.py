from pydantic_settings import BaseSettings, SettingsConfigDict

class SettingsService(BaseSettings):
    
    API_PREFIX: str = "/api/v1"

    GROAI_API_KEY: str

    ENV: str

    QDRANT_API_KEY: str
    
    QDRANT_URL: str

    COLLECTION_NAME: str

    VECTOR_SIZE: int
    
    DB_URL: str

    DB_HOST: str

    DB_PORT: int

    DB_NAME: str

    DB_USERNAME: str

    DB_PASSWORD: str

    JWT_ACCESS_COOKIE_EXPIRE_IN: int

    JWT_REFRESH_COOKIE_EXPIRE_IN: int

    JWT_SECRET_KEY: str

    # JWT signing algorithm.
    JWT_ALGORITHM: str

    # Access token lifetime in minutes.
    JWT_ACCESS_EXPIRE_IN: int

    # Refresh token lifetime in minutes.
    JWT_REFRESH_EXPIRE_IN: int 
    
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def is_dev(self):
        return self.ENV.lower() == "development"
