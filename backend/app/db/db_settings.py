from app.core.settings import Settings
from pydantic import PostgresDsn, computed_field
    

class DbSettingsService:
    def __init__(self, settings: Settings):
        self.settings = settings
    
    # The computed_field decorator
    # Decorator to include property and cached_property when 
    # serializing models or dataclasses.
    # This is useful for fields that are computed from other fields, 
    # or for fields that are expensive to compute and should be cached.</ul>
    @computed_field
    @property
    def get_sql_db_url(self):
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.settings.DB_USERNAME,
            password=self.settings.DB_PASSWORD,
            host=self.settings.DB_NAME,
            port=self.settings.DB_PORT,
            path=self.settings.DB_URL,
        )