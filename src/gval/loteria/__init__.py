# -*- coding: utf-8 -*-
from collections import namedtuple, OrderedDict
import gval.util
import os.path
import gval.loteria.parser
import yaml

Aposta = namedtuple("Aposta", ["concurso", "numeros"])


class Resultado(object):
    def __init__(self, concurso=None, numeros=None, premiacao=None):
        self.concurso = concurso
        self.numeros = numeros
        self.premiacao = premiacao
        self.bruto = None

    def __eq__(self, other):
        if isinstance(other, Resultado):
            return self.__dict__ == other.__dict__

        return False

    def __repr__(self):
        return str(self.__dict__)


class Conferencia(object):
    def __init__(self, aposta, resultado):
        self._set_aposta(aposta)
        self._set_resultado(resultado)

        self._verifica_acertos_premiacao()

    def _verifica_acertos_premiacao(self):
        if self.resultado.concurso != self.aposta.concurso:
            raise RuntimeError("O concurso do resultado é diferente da aposta")

        # Verifica acertos
        self._set_acertados(gval.util.Util.intersecao(self.resultado.numeros,
                                                     self.aposta.numeros))
        self._set_quantidade(len(self.acertados))

        # Verifica se há premiação
        try:
            self._set_premio(self.resultado.premiacao[self.quantidade][1])
        except KeyError:
            self._set_premio(0.00)

    def to_array(self):
        return (self.aposta.concurso, self.quantidade, self.acertados,
                self.premio)

    def get_aposta(self):
        return self._aposta

    def get_resultado(self):
        return self._resultado

    def get_quantidade(self):
        return self._quantidade

    def get_acertados(self):
        return self._acertados

    def get_premio(self):
        return self._premio

    def _set_aposta(self, aposta):
        assert isinstance(aposta, Aposta)
        self._aposta = aposta

    def _set_resultado(self, resultado):
        assert isinstance(resultado, Resultado)
        self._resultado = resultado

    def _set_quantidade(self, quantidade):
        assert isinstance(quantidade, int)
        self._quantidade = quantidade

    def _set_acertados(self, acertados):
        assert isinstance(acertados, (list, tuple, set))
        self._acertados = list(acertados)

    def _set_premio(self, premio):
        assert isinstance(premio, (int, long, float))
        self._premio = premio

    def __eq__(self, other):
        if isinstance(other, Conferencia):
            return self.__dict__ == other.__dict__

        return False

    def __repr__(self):
        return str(self.__dict__)

    aposta = property(get_aposta)
    resultado = property(get_resultado)
    quantidade = property(get_quantidade)
    acertados = property(get_acertados)
    premio = property(get_premio)


class LoteriaException(Exception):
    pass


class Loteria(object):

    # Url comum a todas as loterias conhecidas
    URL_COMUM = "http://www1.caixa.gov.br/loterias/loterias/{loteria}/"

    def __init__(self, nome, cfg=None):
        assert isinstance(nome, basestring)

        # Parâmetros para a loteria pedida
        params = yaml.load(open(os.path.join(os.path.dirname(__file__),
                        "params", "%s.yaml" % nome)))
        # Atribuição dos parâmetros, preenchendo os campos necessários
        self._set_parametros(params)

        # Url base. É necessário para consultar().
        self.url = self._url(loteria=nome,
                             script=params.get("url", {}).get("script"))

        # Objeto responsável por gravar em cache
        self.cacher = gval.util.Cacher(cfg or gval.util.Config())

        # Objeto responsável pelos downloads
        self.downloader = gval.util.Downloader()

        # Parser usado para _obter_resultado()
        self.loteriaparser = getattr(gval.loteria.parser, params["parser"])

    def consultar(self, concurso=None):
        url = self._url_consulta(concurso)

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

    def conferir(self, arg):
        if isinstance(arg, Aposta):
            return self._conferir_uma(arg)

    def _conferir_uma(self, aposta):
        resultado = self.consultar(aposta.concurso)
        conferencia = Conferencia(aposta, resultado)

        return conferencia

    def _obter_resultado(self, html):
        parser = self.loteriaparser()
        parser.feed(html)

        posicao = self.params["posicao"]

        result = Resultado()
        result.bruto = parser.dados
        result.concurso = int(result.bruto[posicao["concurso"]])
        result.numeros = [int(result.bruto[n]) for n in posicao["numeros"]]

        result.premiacao = {}
        for qnt, posicoes in posicao["premios"].iteritems():
            ganhadores = gval.util.Util.str_to_numeral(
                            result.bruto[posicoes[0]], int)
            premio = gval.util.Util.str_to_numeral(result.bruto[posicoes[1]])

            result.premiacao[qnt] = (ganhadores, premio)

        return result

    def _set_parametros(self, params):

        posicao = params["posicao"]
        posicao["concurso"] = posicao.get("concurso", 0)

        nums = posicao["numeros"]
        if len(nums) == 2:
            posicao["numeros"] = xrange(nums[0], nums[1] + 1)

        self.params = params

    def _url(self, loteria, script=None,
                params="?submeteu=sim&opcao=concurso&txtConcurso={concurso}"):
        """Gera da URL_COMUM e os parâmetros a url base para consultar

        Parâmetros:
            loteria - string usada no marcador {loteria} em URL_COMUM.
            script  - nome do script de acesso.
            params  - parâmetros do script, raramente muda.

        Retorna: uma string que possa fazer formatação % com um numeral
        """

        script = script or "{loteria}_pesquisa_new.asp"

        return OrderedDict([
                ("base", (self.URL_COMUM + script).format(loteria=loteria)),
                ("params", params)])

    def _url_consulta(self, concurso=None):
        if concurso is None:
            return self.url["base"]
        else:
            return ''.join(self.url.values()).format(concurso=concurso)
