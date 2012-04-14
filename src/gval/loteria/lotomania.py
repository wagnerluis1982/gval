# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LotomaniaParser

class Lotomania(Loteria):
    _url_script = ("_lotomania_pesquisa.asp")
    _parser_class = LotomaniaParser
    _posicao_numeros = xrange(6, 26)
