# -*- coding: utf-8 -*-
from collections import namedtuple
import gval.util
import os.path

Resultado = namedtuple("Resultado", ["concurso", "numeros"])
Conferencia = namedtuple("Conferencia", ["resultado", "quantidade",
                                         "acertados", "premio"])

class LoteriaException(Exception):
    pass

class Loteria(object):
    # abstract class

    # A constante URL_BASE e os atributos _url_script, _url_params e _loteria
    # servem para construir a url de acesso aos resultados de cada loteria. 
    # Os valores dessa classe são os mais comuns. Cada subclasse deve
    # sobrescrever os valores dos atributos para se adequar à url que deva ser
    # usada.

    # Url comum a todas as loterias conhecidas
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/{loteria}"

    # Nome do script de acesso
    _url_script = "{loteria}_pesquisa_new.asp"

    # Parâmetros do script. Raramente muda
    _url_params = "?submeteu=sim&opcao=concurso&txtConcurso={concurso}"

    # String usada na marca {loteria}. Caso seja None, utiliza o nome da classe
    # com caixa reduzida
    _loteria = None

    # Os dois primeiros atributos abaixo devem ser sobrescritos nas classes
    # filhas, sob pena de exceção na hora de construir a instância.
    # Eles servem como parâmetros para o método _extrair_resultado
    _parser_class = None
    _posicao_numeros = None # list ou generator (ex: xrange) de posições
    _posicao_concurso = 0

    def __init__(self, cfg=None):
        # Valores usados ao consultar() o resultado de um concurso
        self._loteria = self._loteria or self.__class__.__name__.lower()

        # Objeto responsável pelos downloads
        self.downloader = gval.util.Downloader()

        # Objeto responsável por gravar em cache
        cfg = cfg or gval.util.Config()
        self.cacher = gval.util.Cacher(cfg)

        # Verifica se os atributos essenciais estão valorados
        if None in (self._parser_class, self._posicao_numeros):
            raise LoteriaException("Atributos essenciais não valorados")

    def consultar(self, concurso=None):
        url = self.__url_consulta(concurso)

        if concurso is not None:
            content = self.cacher.obter(url)
            if content is None:
                content = self.downloader.download(url)
                self.cacher.guardar(url, content)
        else:
            content = self.downloader.download(url)

        return self._extrair_resultado(content)

    def conferir(self, concurso, numeros):
        resultado = self.consultar(concurso)
        acertados = [num for num in numeros if num in resultado.numeros]

        return Conferencia(resultado=resultado, quantidade=len(acertados),
                           acertados=acertados, premio=0.00)

    def _extrair_resultado(self, html):
        parser = self._parser_class()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=self._posicao_concurso,
            numeros=self._posicao_numeros,
        )

        return Resultado(concurso=int(resultado[POSICAO['concurso']]),
                    numeros=[int(resultado[n]) for n in POSICAO['numeros']])

    def __url_consulta(self, concurso=None):
        fmt_url = os.path.join(self.URL_BASE, self._url_script)
        if concurso is not None:
            fmt_url += self._url_params

        return fmt_url.format(**{'loteria': self._loteria,
                                 'concurso': concurso})
