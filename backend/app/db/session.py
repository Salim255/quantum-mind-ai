from sqlmodel import Session

class DBSessionService:
    def __init__(self, engin):
        self.engin = engin
    
    def get_session(self):
        with Session(self.engine) as session:
            yield  session
    