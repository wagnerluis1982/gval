# -*- coding: utf-8 -*-
import gval.util

# abstract class
class Loteria(object):
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/"

    # Atributo que serve como parâmetro para criar a url e outras coisas. Caso
    # não seja atribuído, utiliza o nome da classe, com a caixa reduzida.
    _loteria = None

    # Parte final da url de consulta. Pode variar de acordo com o jogo.
    _url_loteria = ("{loteria}/{loteria}_pesquisa_new.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    def __init__(self, concurso, cache_dir=None):
        self._loteria = self._loteria or self.__class__.__name__.lower()
        self.__concurso = concurso
        self.url = self.__url_consulta()
        self.cache_dir = cache_dir or gval.util.home_cachedir()
        self.cacher = gval.util.Cacher(self.cache_dir)
        self.downloader = gval.util.Downloader()
        self.html = None

    def consultar(self):
        if self.html is None:
            content = self.cacher.obter(self.url)
            if content is None:
                content = self.downloader.download(self.url)
                self.cacher.guardar(self.url, content)

            self.html = content

        return self._extrair_resultado(self.html)

    # abstract method
    def _extrair_resultado(self, html):
        raise NotImplementedError("Você deve sobrescrever esse método")

    def __url_consulta(self):
        return (self.URL_BASE +
                self._url_loteria.format(loteria=self._loteria,
                                         concurso=self.__concurso))
