from database.base import Base

from sqlalchemy import Column, Integer, String

class Navio(Base):

    __tablename__ = 'navios'

    IMO = Column(Integer, primary_key=True, autoincrement=False)
    nome = Column(String, nullable=False)
    bandeira = Column(String)
    agencia = Column(String)


    def __init__(self, IMO, nome, bandeira, agencia):
        self.IMO = IMO
        self.nome = nome
        self.bandeira = bandeira
        self.agencia = agencia

    def __str__(self):
        return f'Navio: {self.nome} Bandeira: {self.bandeira} IMO: {self.IMO}'

    def __eq__(self, other):
        if not isinstance(other, Navio):
            return False
        
        return self.IMO and other.IMO