
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from database.base import Base


class Agendamento(Base):
    __tablename__ = 'agendamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    engenheiro_id = Column(ForeignKey("engenheiros.id"), nullable=False)
    navio_id = Column(ForeignKey("navios.IMO"), nullable=False)

    engenheiro = relationship("Engenheiro", back_populates="agendamentos")
    navio = relationship("Navio")

    def __init__(self, engenheiro, manobra):
        self.engenheiro = engenheiro
        self.manobra = manobra

    def __str__(self):
        return f'Agendamento {self.id} do engenheiro {self.engenheiro.nome} para a manobra {self.manobra_id}'

