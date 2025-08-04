from datetime import datetime
from typing import List
from database.models import Agendamento
import json
import requests
from time import sleep
class Revolution:

    
    def notifier(self, agendamentos: List[Agendamento]):

        for a in agendamentos:
            nome = a.engenheiro.nome
            telefone = a.engenheiro.telefone
            navio = a.manobra.navio
            data = a.manobra.data
            hora = a.manobra.hora
            # Combinar em um datetime completo
            data_hora = datetime.combine(data, hora)

            data_hora_str = data_hora.strftime('%d/%m/%Y %H:%M')
            manobra = a.manobra.manobra
            mensagem = f'Olá {nome}, segue as últimas atualizações do navio {navio}:\n- PREVISÃO - {data_hora_str}\n- MANOBRA - {manobra}\n- SITUAÇÃO - {a.manobra.situacao}'

            ## Atualizar as informações do banco a cada 5 min e enviar mensagens no whatsapp se sofreu atualização
            data = {"number": telefone,"text": mensagem}
            data_json = json.dumps(data)

            resp = requests.post("http://localhost:8080/message/sendText/POSTMAN TESTE4",
                        data=data_json, 
                        headers= {
                            "Content-Type": "application/json",
                            "apikey": "429683C4C977415CAAFCCE10F7D57E11"
                            })
            sleep(3)
            
            print(resp.json())




