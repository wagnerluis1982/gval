# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao, URL

class Lotomania(Loteria):
    posicao = Posicao(
        numeros = xrange(6, 26),
        premios = {20: (27, 28),
                   19: (29, 30),
                   18: (31, 32),
                   17: (33, 34),
                   16: (35, 36),
                   0:  (37, 38)}
    )

    url = URL(
        script = "_lotomania_pesquisa.asp",
    )
