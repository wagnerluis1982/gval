# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao

class MegaSena(Loteria):
    posicao = Posicao(
        numeros = xrange(28, 34),
        premios = {6: (10, 11),
                   5: (12, 13),
                   4: (14, 15)},
    )
