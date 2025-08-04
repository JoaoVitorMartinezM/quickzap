from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base


class Engenheiro(Base):

    __tablename__ = 'engenheiros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    telefone = Column(String)
    
    agendamentos = relationship("Agendamento", back_populates="engenheiro", cascade="all, delete-orphan")

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        return f'Engenheiro {self.nome}, {self.telefone}'
