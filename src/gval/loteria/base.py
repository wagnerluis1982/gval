# -*- coding: utf-8 -*-
from collections import namedtuple
import gval.util
import os.path
from gval.util import Util

Aposta = namedtuple("Aposta", ["concurso", "numeros"])

class Resultado(object):
    concurso = None
    numeros = None
    premiacao = None
    bruto = None

    def __init__(self, concurso=None, numeros=None, premiacao=None):
        self.concurso = concurso
        self.numeros = numeros
        self.premiacao = premiacao

    def __eq__(self, other):
        assert isinstance(other, Resultado)
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

class Conferencia(object):
    def __init__(self, aposta=None, resultado=None, quantidade=None,
                        acertados=None, premio=None):
        self.aposta = aposta
        self.resultado = resultado
        self.quantidade = quantidade
        self.acertados = acertados
        self.premio = premio

    def calcula_acertos(self):
        if self.resultado is None or self.aposta is None:
            raise RuntimeError("%s.calcula_acertos() não pode ser chamado "
                               "antes de atribuir a aposta e o resultado" %
                               self.__class__.__name__)

        if self.resultado.concurso != self.aposta.concurso:
            raise RuntimeError("O concurso do resultado é diferente da aposta")

        self.acertados = Util.intersecao(self.resultado.numeros,
                                         self.aposta.numeros)
        self.quantidade = len(self.acertados)

    def get_aposta(self):
        return self.__aposta

    def get_resultado(self):
        return self.__resultado

    def get_quantidade(self):
        return self.__quantidade

    def get_acertados(self):
        return self.__acertados

    def get_premio(self):
        return self.__premio

    def set_aposta(self, aposta):
        assert aposta is None or isinstance(aposta, Aposta)
        self.__aposta = aposta

    def set_resultado(self, resultado):
        assert resultado is None or isinstance(resultado, Resultado)
        self.__resultado = resultado

    def set_quantidade(self, quantidade):
        assert quantidade is None or isinstance(quantidade, int)
        self.__quantidade = quantidade

    def set_acertados(self, acertados):
        if acertados is not None:
            assert isinstance(acertados, (list, tuple, set))
            self.__acertados = list(acertados)
        else:
            self.__acertados = None

    def set_premio(self, premio):
        assert premio is None or isinstance(premio, (int, long, float))
        self.__premio = premio

    def del_aposta(self):
        del self.__aposta

    def del_resultado(self):
        del self.__resultado

    def del_quantidade(self):
        del self.__quantidade

    def del_acertados(self):
        del self.__acertados

    def del_premio(self):
        del self.__premio

    def __eq__(self, other):
        assert isinstance(other, Conferencia)
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    aposta = property(get_aposta, set_aposta, del_aposta)
    resultado = property(get_resultado, set_resultado, del_resultado)
    quantidade = property(get_quantidade, set_quantidade, del_quantidade)
    acertados = property(get_acertados, set_acertados, del_acertados)
    premio = property(get_premio, set_premio, del_premio)

class LoteriaException(Exception):
    pass

class Loteria(object):
    # abstract class

    # A constante URL_BASE e os atributos _url_script, _url_params e _url_loteria
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
    _url_loteria = None

    # Os dois primeiros atributos abaixo devem ser sobrescritos nas classes
    # filhas, sob pena de exceção na hora de construir a instância.
    # Eles servem como parâmetros para o método _obter_resultado
    _parser_class = None
    _posicao_numeros = None # list ou generator (ex: xrange) de posições
    _posicao_concurso = 0

    def __init__(self, cfg=None):
        # Valores usados ao consultar() o resultado de um concurso
        self._url_loteria = self._url_loteria or self.__class__.__name__.lower()

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

        return self._obter_resultado(content)

    def conferir(self, aposta):
        conferencia = Conferencia()

        conferencia.aposta = aposta
        conferencia.resultado = self.consultar(aposta.concurso)
        conferencia.calcula_acertos()

        # Verifica se há premiação
        premiacao = conferencia.resultado.premiacao
        try:
            conferencia.premio = premiacao[conferencia.quantidade][1]
        except KeyError:
            conferencia.premio = 0.00

        return conferencia

    def _obter_resultado(self, html):
        POSICAO = dict(
            concurso=self._posicao_concurso,
            numeros=self._posicao_numeros,
        )

        parser = self._parser_class()
        parser.feed(html)

        resultado = Resultado()
        resultado.bruto = parser.dados
        resultado.concurso = int(resultado.bruto[POSICAO["concurso"]])
        resultado.numeros = [int(resultado.bruto[n]) for n in POSICAO['numeros']]

        return resultado

    def __url_consulta(self, concurso=None):
        fmt_url = os.path.join(self.URL_BASE, self._url_script)
        if concurso is not None:
            fmt_url += self._url_params

        return fmt_url.format(**{'loteria': self._url_loteria,
                                 'concurso': concurso})
