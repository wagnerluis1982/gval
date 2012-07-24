# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao, URL

class Lotomania(Loteria):
    posicao = Posicao(
        numeros = xrange(6, 26),
        premios = {},
    )

    url = URL(
        script = "_lotomania_pesquisa.asp",
    )
