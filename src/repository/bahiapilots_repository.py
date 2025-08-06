from typing import List
from database.models import BahiaPilots
from sqlalchemy.orm import Session

class BahiaPilotsRepository():

    def __init__(self, session):
        self.session : Session = session


    def create(self, manobra: BahiaPilots):
        self.session.add_all(manobra)
        self.session.commit()

    def find_all(self):
        return self.session.query(BahiaPilots).all()
        
    def exists_by_navio(self, navio: str):
        return self.session.query(
            self.session.query(BahiaPilots).filter(BahiaPilots.navio == navio).exists()
        ).scalar()
    
    def update_all(self, manobras: List[BahiaPilots]):
        for manobra in manobras:
            self.session.query(BahiaPilots).filter(BahiaPilots.navio == manobra.navio).update({
                "data_hora": manobra.data_hora,
                "navio": manobra.navio,
                "origem": manobra.origem,
                "destino": manobra.destino,
                "data_rebocador": manobra.data_rebocador,
                "rebocadores": manobra.rebocadores,
                "situacao": manobra.situacao,
                "manobra": manobra.manobra
            }, synchronize_session=False)

        self.session.commit()

    

