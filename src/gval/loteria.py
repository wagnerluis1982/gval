# -*- coding: utf-8 -*-
import cookielib
import urllib2

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
        
        resultado = dict()
        resultado['concurso'] = concurso
        resultado['numeros'] = self._extrair_numeros(html)

        return resultado

    def _extrair_numeros(self, html):
        import re
        pattern = r'^(.*?\|){3}(.{%s}).*' % (15*3-1)
        m = re.match(pattern, html)
        resultado_bruto = m.group(2)

        return map(int, resultado_bruto.split('|'))
