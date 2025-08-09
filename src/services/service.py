from pathlib import Path
from api.revolution import Revolution
from database.models import BahiaPilots, Manobra
from database.models.agendamento import Agendamento
from database.models.situacao import Situacao
from repository.agendamento_repository import AgendamentoRepository
from repository.bahiapilots_repository import BahiaPilotsRepository
from repository.manobra_repository import ManobraRepository
from scrapy import Scrapy
from typing import List
from datetime import datetime, date, time
from database.sqlalchemy import ORM
from sqlalchemy.orm import joinedload
import csv



class Service:

    def __init__(self, scrapy: Scrapy, revolution :Revolution):
        self.scrapy = scrapy
        self.revolution = revolution

    def service_bahiapilots_com_br(self):
        dados = self.scrapy.extract_bahiapilots_com_br()
        linhas = dados['linhas']

        def convert(item: List[str]):

            ## Data
            data, hora = item[0].split(' ')
            dia, mes = data.split('/')
            hora, minuto = hora.split(':')
            item[0] = datetime(day=int(dia), month=int(mes), year=datetime.now().year, hour=int(hora), minute=int(minuto))

            ## Trata Rebocadores
            item[-1] = None if item[-1] == '' else item[-1]  

            if item[-1]:
                agora = datetime.now()
                item.append(agora)
                item.append(Situacao.CONFIRMADA.value)
            else:
                item.append(None)
                item.append(Situacao.PREVISTA.value)

            return BahiaPilots(data_hora=item[0], navio=item[1], manobra=item[2], origem=item[3], destino=item[4], rebocadores=item[5], data_rebocador=item[6], situacao=item[7])

        manobras = list(map(convert, linhas))


        with ORM() as db:
            manobra_repo = BahiaPilotsRepository(db.session)
            manobras_banco = manobra_repo.find_all()

            manobras_banco_dict = {(m.navio,m.manobra): m for m in manobras_banco}

            print(manobras_banco_dict)

            # Inserção inicial
            if not manobras_banco:
                manobra_repo.create(manobras)

            # Novas manobras
            novas = [m for m in manobras if (m.navio,m.manobra) not in manobras_banco_dict]
            if novas:
                manobra_repo.create(novas)

            # Atualizar
            atualizar = [
                m for m in manobras
                if (m.navio,m.manobra) in manobras_banco_dict and m != manobras_banco_dict[(m.navio, m.manobra)]
            ]
            for at in atualizar:
                print(at)
            if atualizar:
                manobra_repo.update_all(atualizar)

            self.export_csv(manobra_repo.find_all(), "export_bahia.csv")



    def service_sinprapar_com_br(self):
        dados = self.scrapy.extract_sinprapar_com_br()
        linhas = dados['linhas']
        cabecalho = dados['cabecalho']
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
            

            manobras_banco_dict = {(m.IMO, m.manobra): m for m in manobras_banco if m.IMO and m.manobra}

            # Inserção inicial
            if not manobras_banco:
                manobra_repo.create(manobras)

            # Novas manobras
            novas = [m for m in manobras if (m.IMO, m.manobra) not in manobras_banco_dict]
            if novas:
                manobra_repo.create(novas)

            # Atualizações (comparando com base no __eq__)
            atualizar = [
                m for m in manobras
                if (m.IMO, m.manobra) in manobras_banco_dict and m != manobras_banco_dict[(m.IMO, m.manobra)]
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
            self.export_csv(manobra_repo.find_all(), "export_sinprapar.csv")




        
    def export_csv(self, dados, filename):
        db_path = Path(__file__).resolve().parent.parent / filename
        with open(db_path, 'a', newline='', encoding='utf-8') as file:
            file_exists = db_path.exists() and db_path.stat().st_size > 0
            objeto =vars(dados[0]).copy()
            objeto.pop("_sa_instance_state", None)
            fieldnames = objeto.keys()
            print(objeto)
            print(fieldnames)
            writer = csv.DictWriter(file, fieldnames=['ID', 'Nome do navio', 'Manobra', 'Data rebocador', 'Data manobra', 'Origem', 'Destino', 'Rebocador', 'Situação'])
            if not file_exists:
                writer.writeheader()
            
            for d in dados:
                objeto = vars(d).copy()
                objeto.pop("_sa_instance_state", None)

                objeto_new = {
                    'ID': objeto['id'],
                    'Nome do navio': objeto['navio'],
                    'Manobra': objeto['manobra'],
                    'Data rebocador': objeto['data_rebocador'],
                    'Data manobra': objeto['data_hora'],
                    'Origem': objeto['origem'],
                    'Destino': objeto['destino'],
                    'Rebocador': objeto['rebocadores'],
                    'Situação': objeto['situacao']
                }

                writer.writerow(objeto_new)


