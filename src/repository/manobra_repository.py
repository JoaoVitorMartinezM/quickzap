from database.models import Manobra
from sqlalchemy.orm import Session
from typing import List

class ManobraRepository:

    def __init__(self, session):
        self.session: Session = session



    def create(self, manobra: Manobra):
        self.session.add_all(manobra)
        self.session.commit()

    def find_all(self):
        return self.session.query(Manobra).all()
        
    def exists_by_IMO(self, IMO: int):
        return self.session.query(
            self.session.query(Manobra).filter(Manobra.IMO == IMO).exists()
        ).scalar()
    
    def update_all(self, manobras: List[Manobra]):
        for manobra in manobras:
            self.session.query(Manobra).filter(Manobra.IMO == manobra.IMO).update({
                "agencia": manobra.agencia,
                "amarracao": manobra.amarracao,
                "bandeira": manobra.bandeira,
                "boca": manobra.boca,
                "calado": manobra.calado,
                "data": manobra.data,
                "DWT": manobra.DWT,
                "fundeio_barra": manobra.fundeio_barra,
                "hora": manobra.hora,
                "indicativo": manobra.indicativo,
                "LOA": manobra.LOA,
                "navio": manobra.navio,
                "rebocadores": manobra.rebocadores,
                "situacao": manobra.situacao,
                "TBA": manobra.TBA,
                "tipo": manobra.tipo,
                "manobra": manobra.manobra
            }, synchronize_session=False)

        self.session.commit()