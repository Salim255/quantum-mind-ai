from pydantic import PostgresDsn

from app.core.settings import Settings


class DbSettingsService:
    """
    Responsible for building and exposing database-related
    configuration values.

    This service acts as the single source of truth for
    database connection settings. Any component that needs
    the database URL should obtain it from here rather than
    constructing it manually.

    Flow:

        Settings (.env)
              ↓
        DbSettingsService
              ↓
        SQL Database URL
              ↓
        DBEngineService
              ↓
        PostgreSQL
    """

    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def sql_db_url(self) -> str:
        """
        Build and return the PostgreSQL connection URL.

        The URL is dynamically generated from the application's
        database settings to ensure a single source of truth.

        Example:

            postgresql+psycopg://user:password@localhost:5432/database

        Returns:
            PostgresDsn: Validated PostgreSQL connection string.
        """
        return str(PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.settings.DB_USERNAME,
            password=self.settings.DB_PASSWORD,
            host=self.settings.DB_HOST,
            port=self.settings.DB_PORT,
            path=self.settings.DB_NAME,
        ))