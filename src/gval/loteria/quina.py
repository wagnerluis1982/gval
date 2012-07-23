# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao

class Quina(Loteria):
    posicao = Posicao(
        numeros = xrange(21, 26),
        premios = {},
    )
