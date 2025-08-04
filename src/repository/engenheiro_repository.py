from database.models import Engenheiro
from sqlalchemy.orm import Session

class EngenheiroRepository:
    
    def __init__(self, session):
        self.session : Session = session

    def create(self, engenheiro: Engenheiro):
        self.session.add(engenheiro)
        self.session.commit()
        