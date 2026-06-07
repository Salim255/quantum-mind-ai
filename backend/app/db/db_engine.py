from sqlmodel import create_engine
from app.core.settings import Settings

class DBEngineService:
    def __init__(self, settings: Settings):
        self.settings = settings

        self.get_engine()
        
        self.connect_args = {"check_same_thread": False}

    def get_engine(self):
        create_engine(self.settings.DB_URL, connect_args=self.connect_args)