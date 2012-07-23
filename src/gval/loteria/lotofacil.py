# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.util import Util

class Lotofacil(Loteria):
    _posicao_numeros = xrange(3, 18)

    def _obter_resultado(self, html):
        resultado = Loteria._obter_resultado(self, html)
        resultado.premiacao = {}
        for mapa in ((15, 18, 19),
                     (14, 20, 21),
                     (13, 22, 23),
                     (12, 24, 25),
                     (11, 26, 27)):
            quantidade = Util.str_to_numeral(resultado.bruto[mapa[1]], int)
            premio = Util.str_to_numeral(resultado.bruto[mapa[2]])

            resultado.premiacao[mapa[0]] = (quantidade, premio)

        return resultado
