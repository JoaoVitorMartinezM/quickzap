from database.models import Manobra
from database.models.navio import Navio
from sqlalchemy.orm import Session
from typing import List

class ManobraRepository:

    def __init__(self, session):
        self.session: Session = session



    def create(self, manobra: Manobra):
        for m in manobra:
            
            navio_existente = self.session.get(Navio, m.navio.IMO)
            if navio_existente:
                m.navio = navio_existente  
            

        self.session.add_all(manobra)
        self.session.commit()

    def find_all(self):
        return self.session.query(Manobra).all()
        
    def exists_by_IMO_manobra(self, IMO: int, manobra: str):
        return self.session.query(
            self.session.query(Manobra).filter(Manobra.IMO == IMO, Manobra.manobra == manobra).exists()
        ).scalar()
    
    def update_all(self, manobras: List[Manobra]):
        for manobra in manobras:
            self.session.query(Manobra).filter(Manobra.navio == manobra.navio, Manobra.manobra == manobra.manobra).update({
                "amarracao": manobra.amarracao,
                "boca": manobra.boca,
                "calado": manobra.calado,
                "data": manobra.data,
                "DWT": manobra.DWT,
                "fundeio_barra": manobra.fundeio_barra,
                "hora": manobra.hora,
                "indicativo": manobra.indicativo,
                "LOA": manobra.LOA,
                "rebocadores": manobra.rebocadores,
                "situacao": manobra.situacao,
                "TBA": manobra.TBA,
                "tipo": manobra.tipo,
                "manobra": manobra.manobra,
                "navio_id": manobra.navio.IMO
            }, synchronize_session=False)

        self.session.commit()