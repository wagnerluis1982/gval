# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LotofacilParser

def obter_numeral(str_numero, xtype=float):
    assert isinstance(str_numero, basestring)

    _ord = lambda x: isinstance(x, basestring) and ord(x) or None
    tabela = dict(map(lambda x,y: (_ord(x), _ord(y)),
                      (',','.'), ('.',None) ))

    return xtype(str_numero.translate(tabela))

class Lotofacil(Loteria):
    _parser_class = LotofacilParser
    _posicao_numeros = xrange(3, 18)

    def _obter_resultado(self, html):
        resultado = Loteria._obter_resultado(self, html)
        resultado.premiacao = {}
        for mapa in ((15, 18, 19),
                     (14, 20, 21),
                     (13, 22, 23),
                     (12, 24, 25),
                     (11, 26, 27)):
            quantidade = obter_numeral(resultado.bruto[mapa[1]], int)
            premio = obter_numeral(resultado.bruto[mapa[2]])

            resultado.premiacao[mapa[0]] = (quantidade, premio)

        return resultado
