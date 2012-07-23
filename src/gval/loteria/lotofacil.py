# -*- coding: utf-8 -*-
from gval.loteria import Loteria

class Lotofacil(Loteria):
    _posicao_numeros = xrange(3, 18)
    _posicao_premios = ((15, 18, 19),
                        (14, 20, 21),
                        (13, 22, 23),
                        (12, 24, 25),
                        (11, 26, 27))
