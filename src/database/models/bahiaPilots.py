from sqlalchemy import Column, Integer, String, Date, Time, Float, CHAR, DateTime

from database.base import Base

class BahiaPilots(Base):
    __tablename__ = 'bahiapilots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, nullable=False)
    navio = Column(String)
    manobra = Column(String)
    origem = Column(String)
    destino = Column(String)
    rebocadores = Column(String)
    data_rebocador = Column(DateTime)
    situacao = Column(String)


    def __init__(self, data_hora, navio, manobra, origem, destino,
                rebocadores, data_rebocador, situacao):
        self.data_hora = data_hora
        self.navio = navio
        self.manobra = manobra
        self.origem = origem
        self.destino = destino
        self.rebocadores = rebocadores
        self.data_rebocador = data_rebocador
        self.situacao = situacao

    def __str__(self):
        return f'Navio: {self.navio} Manobra: {self.manobra} Origem: {self.origem} Destino: {self.destino}'
    
    def __eq__(self, other):
        if not isinstance(other, BahiaPilots):
            return False
        return (self.data_hora == other.data_hora and self.navio == other.navio
                and self.manobra == other.manobra and self.rebocadores == other.rebocadores  
                and self.data_rebocador == other.data_rebocador and self.situacao == other.situacao
                and self.origem == other.origem and self.destino == other.destino)
 
