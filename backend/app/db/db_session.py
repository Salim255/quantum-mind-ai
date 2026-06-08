from sqlmodel import Session
from sqlalchemy.engine import Engine

class DBSessionService:
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def get_session(self):
        with Session(self.engine) as session:
            yield  session
    