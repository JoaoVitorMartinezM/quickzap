from api.revolution import Revolution
from database.models import Manobra
from database.models.agendamento import Agendamento
from repository.agendamento_repository import AgendamentoRepository
from repository.manobra_repository import ManobraRepository
from scrapy import Scrapy
from typing import List
from datetime import datetime, date, time
from database.sqlalchemy import ORM
from sqlalchemy.orm import joinedload



class Service:

    def __init__(self, scrapy: Scrapy, revolution :Revolution):
        self.scrapy = scrapy
        self.revolution = revolution

    # def data_convertions(self):
    #     self.scrapy.extract()
    #     linhas = self.scrapy.linhas
    #     print(self.scrapy.cabecalho)

        
    #     def convert(item: List[str]):
    #         ## Data
    #         dia, mes = item[0].split('/')
    #         item[0] = date(day=int(dia), month=int(mes), year=int(datetime.now().year))
    #         if not item[16].__eq__(''):
    #             item[16] = datetime.strptime(item[16], '%d/%m/%Y %H:%M')
    #         else:
    #             item[16] = None
            
            

    #         ## Hora
    #         hora, minuto = item[1].split(":")
    #         item[1] = time(hour=int(hora), minute=int(minuto))

    #         ## STR TO FLOAT
    #         item[5] = float(item[5].replace(',', '.'))
    #         item[6] = float(item[6].replace(',', '.'))
    #         item[7] = float(item[7].replace(',', '.'))
    #         item[8] = int(item[8])
    #         item[9] = int(item[9])
    #         item[10] = int(item[10])

    #         manobra = Manobra(data=item[0], hora=item[1], navio=item[2], manobra=item[3], tipo=item[4], LOA=item[5], 
    #                boca=item[6], calado=item[7], TBA=item[8], DWT=item[9], IMO=item[10], rebocadores=item[11], 
    #                amarracao=item[12], agencia=item[13], bandeira=item[14], indicativo=item[15], fundeio_barra=item[16], situacao=item[17])

            
    #         return manobra
        
    #     manobras = list(map(convert, linhas))

    #     with ORM() as db:
    #         manobra_repo = ManobraRepository(db.session)
    #         agendamento_repo = AgendamentoRepository(db.session)
    #         manobras_banco = manobra_repo.find_all()

    #         # Save the Scrapy if first time
    #         if len(manobras_banco) == 0:
    #             manobra_repo.create(manobras)

    #         # SAVE
    #         salvar = list(filter(lambda x: not manobra_repo.exists_by_IMO(x.IMO), manobras))
    #         if salvar.__len__() != 0:
    #             manobra_repo.create(salvar)

    #         # UPDATE
    #         atualizar = list(filter(lambda x: x not in manobras_banco, manobras))
    #         if atualizar.__len__() != 0:
    #             manobra_repo.update_all(atualizar)

    #         ids_manobras_atualizadas = list(map(lambda x: x.IMO, atualizar))
    #         agendamentos_notificar = []
    #         for id in ids_manobras_atualizadas:
    #             agendamento = db.session.query(Agendamento).where(Manobra.IMO == id).first()
    #             if agendamento is not None: 
    #                 agendamentos_notificar.append(agendamento)
    #         print(f'TAMANHO LISTA NOTIFICACAO: {len(agendamentos_notificar)}')
    #         print(f'TAMANHO LISTA UPDATE: {len(atualizar)}')
    #         print(f'TAMANHO LISTA IDs: {len(ids_manobras_atualizadas)}')

    #         self.revolution.notifier(agendamentos_notificar)



        
    #     return manobras
            
    def data_convertions(self):
        self.scrapy.extract()
        linhas = self.scrapy.linhas
        print(self.scrapy.cabecalho)

        def convert(item: List[str]):
            # Data
            dia, mes = item[0].split('/')
            item[0] = date(day=int(dia), month=int(mes), year=datetime.now().year)

            # fundeio_barra (item[16])
            if item[16] != '':
                item[16] = datetime.strptime(item[16], '%d/%m/%Y %H:%M')
            else:
                item[16] = None

            # Hora
            hora, minuto = item[1].split(":")
            item[1] = time(hour=int(hora), minute=int(minuto))

            # Conversões de string para float/int
            item[5] = float(item[5].replace(',', '.'))
            item[6] = float(item[6].replace(',', '.'))
            item[7] = float(item[7].replace(',', '.'))
            item[8] = int(item[8])
            item[9] = int(item[9])
            item[10] = int(item[10])

            return Manobra(
                data=item[0], hora=item[1], navio=item[2], manobra=item[3], tipo=item[4],
                LOA=item[5], boca=item[6], calado=item[7], TBA=item[8], DWT=item[9],
                IMO=item[10], rebocadores=item[11], amarracao=item[12], agencia=item[13],
                bandeira=item[14], indicativo=item[15], fundeio_barra=item[16], situacao=item[17]
            )

        manobras = list(map(convert, linhas))

        with ORM() as db:
            manobra_repo = ManobraRepository(db.session)
            agendamento_repo = AgendamentoRepository(db.session)
            manobras_banco = manobra_repo.find_all()

            manobras_banco_dict = {m.IMO: m for m in manobras_banco}

            # Inserção inicial
            if not manobras_banco:
                manobra_repo.create(manobras)

            # Novas manobras
            novas = [m for m in manobras if m.IMO not in manobras_banco_dict]
            if novas:
                manobra_repo.create(novas)

            # Atualizações (comparando com base no __eq__)
            atualizar = [
                m for m in manobras
                if m.IMO in manobras_banco_dict and not m == manobras_banco_dict[m.IMO]
            ]
            if atualizar:
                manobra_repo.update_all(atualizar)

            # Buscar agendamentos que precisam ser notificados
            ids_atualizados = set(m.IMO for m in atualizar)
            agendamentos_notificar = (
            db.session.query(Agendamento)
            .join(Manobra, Agendamento.manobra_id == Manobra.id)
            .filter(Manobra.IMO.in_(ids_atualizados))
            .options(joinedload(Agendamento.engenheiro), joinedload(Agendamento.manobra))
            .all()
)

            print(f"[NOTIFICAR] {len(agendamentos_notificar)} agendamento(s)")
            self.revolution.notifier(agendamentos_notificar)

    