from sqlmodel import create_engine

class DBEngineService:
    db_url = ""

    connect_args = {"check_same_thread": False}

    @classmethod
    def get_engin(cls):

        return create_engine(cls.db_url, connect_args=cls.connect_args)