from database.models import Agendamento
from sqlalchemy.orm import Session


class AgendamentoRepository:

    def __init__(self, session):
        self.session : Session = session

    def find_all(self):
        data = self.session.query(Agendamento).all()
        return data
