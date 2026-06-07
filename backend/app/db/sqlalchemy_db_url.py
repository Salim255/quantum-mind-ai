from app.core.settings import Settings
from pydantic import PostgresDsn
    

class SQLAlchemyDatabaseUrlService:
    def __init__(self, settings: Settings):
        self.settings = Settings
    
    def get_sql_db_url(self)-> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.settings.DB_USERNAME,
            password=self.settings.DB_PASSWORD,
            host=self.settings.DB_NAME,
            port=self.settings.DB_PORT,
            path=self.settings.DB_URL,
        )