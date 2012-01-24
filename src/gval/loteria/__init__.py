# -*- coding: utf-8 -*-

# abstract class
class Loteria(object):
    def __init__(self):
        if not issubclass(self.__class__, Loteria):
            raise NotImplementedError, ("Essa classe não pode ser instanciada "
                                        "diretamente")

    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"
    URL_CONSULTA = ("{loteria}/{loteria}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    # abstract method
    def consultar(self, concurso, url=None):
        raise NotImplementedError, "Você deve sobrescrever esse método"

    def _url_consulta(self, loteria, concurso):
        dados_aposta = {'loteria':loteria, 'concurso':concurso}
        return self.URL_BASE + self.URL_CONSULTA.format(**dados_aposta)
