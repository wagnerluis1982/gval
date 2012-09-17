# -*- coding: utf-8 -*-
from collections import namedtuple
import gval.util
import os.path
import gval.loteria.parser
import yaml

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

        self.acertados = gval.util.Util.intersecao(self.resultado.numeros,
                                                   self.aposta.numeros)
        self.quantidade = len(self.acertados)

    def to_array(self):
        return (self.aposta.concurso, self.quantidade, self.acertados, self.premio)

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

class URL(object):
    # A constante BASE e os atributos script, params e loteria servem para
    # construir a url de acesso aos resultados de cada loteria.
    # Os valores dessa classe são os mais comuns. Cada subclasse de Loteria
    # deve sobrescrever os atributos para se adequar à url que deva ser usada.

    # Url comum a todas as loterias conhecidas
    BASE = "http://www1.caixa.gov.br/loterias/loterias/{loteria}"

    def __init__(self, script=None,
                  params="?submeteu=sim&opcao=concurso&txtConcurso={concurso}",
                  loteria=None):
        self.script = script or "{loteria}_pesquisa_new.asp" # Nome do script
        self.params = params    # Parâmetros do script. Raramente muda.
        self.loteria = loteria  # String usada em {loteria}.


class Posicao(object):
    # Os atributos numeros e premios são mandatórios

    def __init__(self, concurso=0, numeros=None, premios=None):
        if len(numeros) == 2:
            numeros = xrange(numeros[0], numeros[1]+1)

        self.concurso = concurso # int
        self.numeros = numeros   # list(<int>,...) ou generator(<int>)
        self.premios = premios   # dict(<int>: (<int>, <int>))


class LoteriaException(Exception):
    pass


class Loteria(object):

    # Instância da classe URL. É necessário para consultar().
    url = None

    # Instância da classe Posicao. É necessário para _obter_resultado().
    posicao = None

    # Classe do parser usada para _obter_resultado(). Normalmente é obtida de
    # forma automática a partir de gval.loteria.parser.<subclassName>Parser.
    parser_class = None

    def __init__(self, nome, cfg=None):
        parser_name = None

        # TODO: if temporário (será substituído por is None para gerar raise)
        if nome is not None:
           params = yaml.load(open(os.path.join(os.path.dirname(__file__),
               "params", "%s.yaml" % nome)))
           self.posicao = Posicao(**params["posicao"])
           parser_name = params["parser"]
           if params.get("url") is not None:
               self.url = URL(loteria=nome, script=params["url"].get("script"))

        # Verifica se os atributos essenciais estão valorados
        if None in (self.posicao.numeros, self.posicao.premios):
            raise LoteriaException("Atributos essenciais não valorados")

        # Objeto responsável por gravar em cache
        cfg = cfg or gval.util.Config()
        self.cacher = gval.util.Cacher(cfg)

        # Objeto responsável pelos downloads
        self.downloader = gval.util.Downloader()

        # Instancia url se preciso
        if self.url is None:
            self.url = URL(loteria=nome)

        # Valores usados ao consultar() o resultado de um concurso
        self.url.loteria = self.url.loteria or self.__class__.__name__.lower()
        self.parser_class = (self.parser_class or
                getattr(gval.loteria.parser,
                    parser_name or "%sParser" % self.__class__.__name__))

    def consultar(self, concurso=None):
        url = self.__url_consulta(concurso)

        content = self.cacher.obter(url)
        if content is not None:
            return self._obter_resultado(content)
        else:
            content = self.downloader.download(url)

            try:
                resultado = self._obter_resultado(content)
            except ValueError:
                raise LoteriaException("%s %d não disponível" %
                                                    (self.__class__.__name__,
                                                     concurso))
            else:
                self.cacher.guardar(url, content)
                return resultado

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
        parser = self.parser_class()
        parser.feed(html)

        resultado = Resultado()
        resultado.bruto = parser.dados
        resultado.concurso = int(resultado.bruto[self.posicao.concurso])
        resultado.numeros = [int(resultado.bruto[n]) for n in self.posicao.numeros]

        resultado.premiacao = {}
        for qnt, posicoes in self.posicao.premios.iteritems():
            ganhadores = gval.util.Util.str_to_numeral(
                            resultado.bruto[posicoes[0]], int)
            premio = gval.util.Util.str_to_numeral(resultado.bruto[posicoes[1]])

            resultado.premiacao[qnt] = (ganhadores, premio)

        return resultado

    def __url_consulta(self, concurso=None):
        fmt_url = "%s/%s" % (self.url.BASE, self.url.script)
        if concurso is not None:
            fmt_url += self.url.params

        return fmt_url.format(**{'loteria': self.url.loteria,
                                 'concurso': concurso})
