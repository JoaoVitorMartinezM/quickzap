import requests
from bs4 import BeautifulSoup

class Scrapy:

    def __init__(self):
        self.cabecalho = []
        self.linhas = []

    def extract(self):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com"
        }
        
        html = requests.get("https://www.sinprapar.com.br/PREV.HTM", headers=headers)
        
        if html.status_code != 200 :
            print(f'Deu ruim')
            
        print("Ok")

        soup = BeautifulSoup(html.content, "html.parser")

        linhas = soup.find_all("tr")

        cabecalho = linhas[1].get_text().split("\n")
        self.cabecalho = list(filter(lambda x: x != "", cabecalho))

        linhas.pop(0)
        linhas.pop(0)

        def trata_linhas(item):
            colunas = item.get_text().split("\n")
            colunas.pop()
            colunas.pop(0)
            return colunas
        
        self.linhas = list(map(trata_linhas, linhas))
        




  
