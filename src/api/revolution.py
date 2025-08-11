from datetime import datetime
from typing import List
from database.models import Agendamento
import json
import requests

class Revolution:

    
    def notifier(self, agendamentos: List[Agendamento]):

        for a, m in agendamentos:
            nome = a.engenheiro.nome
            telefone = a.engenheiro.telefone
            navio = a.navio.nome
            data = m.data
            hora = m.hora
            # Combinar em um datetime completo
            data_hora = datetime.combine(data, hora)

            data_hora_str = data_hora.strftime('%d/%m/%Y %H:%M')
            manobra = m.manobra
            mensagem = f'Navio *{navio}* - ({nome})\n- PREVISÃO - {data_hora_str}\n- MANOBRA - {manobra}\n- SITUAÇÃO - {m.situacao}'

            ## Atualizar as informações do banco a cada 5 min e enviar mensagens no whatsapp se sofreu atualização
            data = {"number": telefone,"text": mensagem}
            data_json = json.dumps(data)

            resp = requests.post("http://localhost:8080/message/sendText/POSTMAN TESTE4",
                        data=data_json, 
                        headers= {
                            "Content-Type": "application/json",
                            "apikey": "429683C4C977415CAAFCCE10F7D57E11"
                            })
                        
            print(resp.json())




