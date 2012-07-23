# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao

class MegaSena(Loteria):
    posicao = Posicao(
        numeros = xrange(28, 34),
        premios = {},
    )
