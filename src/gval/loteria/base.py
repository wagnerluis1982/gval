# -*- coding: utf-8 -*-
import gval

# abstract class
class Loteria(object):
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"

    # Atributo que serve como parâmetro para criar a url e outras coisas. Caso
    # não seja atribuído, utiliza o nome da classe, com a caixa reduzida.
    _loteria = None

    # Parte final da url de consulta. Pode variar de acordo com o jogo.
    _url_loteria = ("{loteria}/{loteria}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    def __init__(self, concurso, url=None):
        self._loteria = self._loteria or self.__class__.__name__.lower()
        self.__concurso = concurso
        self.url = url or self.__url_consulta()
        self.html = None

    def consultar(self):
        self.html = self.html or gval.download_pagina(self.url)

        return self._extrair_resultado(self.html)

    # abstract method
    def _extrair_resultado(self, html):
        raise NotImplementedError("Você deve sobrescrever esse método")

    def __url_consulta(self):
        return (self.URL_BASE +
                self._url_loteria.format(loteria=self._loteria,
                                         concurso=self.__concurso))
