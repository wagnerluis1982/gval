# -*- coding: utf-8 -*-

# abstract class
class Loteria(object):
    def __init__(self, concurso, url=None):
        self.url = url or self._url_consulta(self._loteria, concurso)
        self.html = None

    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"
    URL_CONSULTA = ("{loteria}/{loteria}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    # abstract method
    def consultar(self):
        raise NotImplementedError, "Você deve sobrescrever esse método"

    def _url_consulta(self, loteria, concurso):
        dados_aposta = {'loteria':loteria, 'concurso':concurso}
        return self.URL_BASE + self.URL_CONSULTA.format(**dados_aposta)
