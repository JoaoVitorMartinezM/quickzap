from sqlalchemy import Column, Integer, String, Date, Time, Float, CHAR, DateTime

from database.base import Base

class Manobra(Base):
    __tablename__ = 'manobras'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    navio = Column(String)
    manobra = Column(String)
    tipo = Column(String)
    LOA = Column(Float)
    boca = Column(Float)
    calado = Column(Float)
    TBA = Column(Integer)
    DWT = Column(Integer)
    IMO = Column(Integer, unique=True)
    rebocadores = Column(String)
    amarracao = Column(CHAR)
    agencia = Column(String)
    bandeira = Column(String)
    indicativo = Column(String)
    fundeio_barra = Column(DateTime)
    situacao = Column(String)


    def __init__(self,data, hora, navio, manobra,
                  tipo, LOA, boca, calado, TBA, DWT,
                    IMO, rebocadores, amarracao, agencia, bandeira,
                      indicativo, fundeio_barra, situacao):
        self.data = data
        self.hora = hora
        self.navio = navio
        self.manobra = manobra
        self.tipo = tipo
        self.LOA = LOA
        self.boca = boca
        self.calado = calado
        self.TBA = TBA
        self.DWT = DWT
        self.IMO = IMO
        self.rebocadores = rebocadores
        self.amarracao = amarracao
        self.agencia = agencia
        self.bandeira = bandeira
        self.indicativo = indicativo
        self.fundeio_barra = fundeio_barra
        self.situacao = situacao

    def __str__(self):
        return f'Navio: {self.navio} Bandeira: {self.bandeira} IMO: {self.IMO}'
    
    def __eq__(self, other):
        if not isinstance(other, Manobra):
            return False
        return (self.data == other.data and self.hora == other.hora and self.navio == other.navio
                and self.manobra == other.manobra and self.tipo == other.tipo and self.LOA == other.LOA 
                and self.boca == other.boca and self.calado == other.calado and self.TBA == other.TBA 
                and self.DWT == other.DWT and self.IMO == other.IMO and self.rebocadores == other.rebocadores 
                and self.amarracao == other.amarracao and self.agencia == other.agencia and self.bandeira == other.bandeira 
                and self.indicativo == other.indicativo and self.fundeio_barra == other.fundeio_barra and self.situacao == other.situacao)
