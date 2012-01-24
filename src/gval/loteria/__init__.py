# -*- coding: utf-8 -*-
import cookielib
import re
import urllib2

from gval.loteria.parser import LoteriaParser

def download_pagina(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(url)

    return page.read()

class Loteria(object):
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"
    URL_CONSULTA = ("{jogo}/{jogo}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    def _url_consulta(self, jogo, concurso):
        dados_aposta = {'jogo':jogo, 'concurso':concurso}
        return self.URL_BASE + self.URL_CONSULTA.format(**dados_aposta)

class Lotofacil(Loteria):
    def consultar(self, concurso, url=None):
        url = url or self._url_consulta('lotofacil', concurso)
        html = download_pagina(url)
        
        return self._extrair_resultado(html)

    def _extrair_resultado(self, html):
        dados = LoteriaParser().feed(html)

        pattern = (r"(\d+)\|+"           # concurso
                   r"((?:\d{2}\|){15})") # numeros sorteados
        matched = re.match(pattern, dados).groups()

        return {'concurso': matched[0],
                'numeros': [int(num) for num in matched[1].split('|') if num]}
