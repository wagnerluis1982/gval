# -*- coding: utf-8 -*-
import gval

# abstract class
class Loteria(object):
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"

    _loteria = None
    _url_loteria = ("{loteria}/{loteria}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    def __init__(self, concurso, url=None):
        self.url = url or self.__url_consulta(self._loteria, concurso)
        self.html = None

    def consultar(self):
        self.html = self.html or gval.download_pagina(self.url)

        return self._extrair_resultado(self.html)

    # abstract method
    def _extrair_resultado(self, html):
        raise NotImplementedError("Você deve sobrescrever esse método")

    def __url_consulta(self, loteria, concurso):
        dados_aposta = {'loteria':loteria, 'concurso':concurso}
        return self.URL_BASE + self._url_loteria.format(**dados_aposta)
