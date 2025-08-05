import requests
from bs4 import BeautifulSoup

class Scrapy:

    def __init__(self):
        self.cabecalho = []
        self.linhas = []

    def extract_bahiapilots_com_br(self):
        soup = self.request_bsoup('https://bahiapilots.com.br/movimentacao-dos-navios/')
        linhas = soup.find_all("tr")
        cabecalho = linhas[0]
        linhas.pop(0)

        def trata_linhas(item):
            colunas = BeautifulSoup(str(item), "html.parser")
            colunas = colunas.find_all("td")
            colunas = list(map(lambda x: x.get_text(),colunas))
            return colunas

        linhas = list(map(trata_linhas, linhas))
        
        return {
            'cabecalho': cabecalho,
            'linhas': linhas
        }
            

    def extract_sinprapar_com_br(self):

        soup = self.request_bsoup('https://www.sinprapar.com.br/PREV.HTM')

        linhas = soup.find_all("tr")

        cabecalho = linhas[1].get_text().split("\n")
        cabecalho = list(filter(lambda x: x != "", cabecalho))

        linhas.pop(0)
        linhas.pop(0)

        def trata_linhas(item):
            colunas = item.get_text().split("\n")
            colunas.pop()
            colunas.pop(0)
            return colunas
        
        linhas = list(map(trata_linhas, linhas))

        return {
            'cabecalho': cabecalho,
            'linhas': linhas
        }
    
    def request_bsoup(self, url):
            
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com"
        }
        
        resp = requests.get(url, headers=headers)
        
        if resp.status_code != 200 :
            raise Exception(f'A requisição para {url} falhou.')
            
        print(f'Acesso em {url}')
        soup = BeautifulSoup(resp.content, "html.parser")
        return soup

        




  
