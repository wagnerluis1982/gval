# -*- coding: utf-8 -*-
from gval.loteria import Loteria

class Lotomania(Loteria):
    _url_script = ("_lotomania_pesquisa.asp")
    _posicao_numeros = xrange(6, 26)
    _posicao_premios = ()
