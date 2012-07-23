# -*- coding: utf-8 -*-
from gval.loteria import Loteria, Posicao

class Lotomania(Loteria):
    posicao = Posicao(
        numeros = xrange(6, 26),
        premios = {},
    )

    url_script = "_lotomania_pesquisa.asp"
