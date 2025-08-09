from datetime import date, time, datetime
from api.revolution import Revolution
from database.models.engenheiro import Engenheiro
from database.models.manobra import Manobra
from database.models.agendamento import Agendamento
from repository import AgendamentoRepository, EngenheiroRepository, ManobraRepository
from scrapy import Scrapy
from services.service import Service
from  database.sqlalchemy import ORM

# db_path = Path(__file__).resolve().parent / "database" / "sinprapar.db"


# print(data[0])

# sql = DB(str(db_path))

# sql.generate_db()

# sql.populate(data)
# data = sql.test()
# print(data)



# session = orm.session

# engenheiro = Engenheiro(nome='Vitor', telefone='99999999')
# manobra = Manobra(
#     data=date(2019, 12, 4),              # valor direto
#     hora=time(12),                      # idem
#     navio="NAVIO TESTE",
#     manobra="DF",
#     tipo="TQ",
#     LOA=123.23,
#     boca=12.12,
#     calado=11.11,
#     TBA=12345,
#     DWT=12345,
#     IMO=123456,
#     rebocadores="WVS",
#     amarracao="P",
#     agencia="GRANEL",
#     bandeira="SINGAPURE",
#     indicativo="VH5HJ9",
#     fundeio_barra=datetime.now(),
#     situacao="PREVISTO"
# )

# agendamento = Agendamento(manobra=manobra, engenheiro=engenheiro)

# manobra = session.query(Manobra).first()

# session.add(agendamento)
# session.commit()

# engenheiro = session.query(Engenheiro).first()
# manobra = session.query(Manobra).first()

# agendamento = Agendamento(engenheiro=engenheiro, manobra=manobra)

# print(engenheiro.agendamentos[0])

# session.add(agendamento)
# session.commit()

# engenheiro = Engenheiro(nome="João",telefone="88888888")
# manobra = session.query(Manobra).first()
# agendamento2 = Agendamento(engenheiro=engenheiro, manobra=manobra)
# session.add(agendamento2)
# session.commit()

# agendamento= session.query(Agendamento).where(Agendamento.id == 2).first()

# print(agendamento.engenheiro)
# with ORM() as db:

#     agendamento_repo = AgendamentoRepository(db.session)


#     todos_agendamentos = agendamento_repo.find_all()

#     print(todos_agendamentos)

#     eng_repo = EngenheiroRepository(db.session)

#     eng_repo.create(
#         Engenheiro(nome='Pedro', telefone='481111111')
#     )


orm = ORM()
orm.generateBD()
scrapy =  Scrapy()
revolution = Revolution()
service = Service(scrapy, revolution)
service.service_sinprapar_com_br()
service.service_bahiapilots_com_br()