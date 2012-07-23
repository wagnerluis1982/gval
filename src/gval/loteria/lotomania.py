# -*- coding: utf-8 -*-
from gval.loteria import Loteria

class Lotomania(Loteria):
    posicao_numeros = xrange(6, 26)
    posicao_premios = {}

    url_script = "_lotomania_pesquisa.asp"
