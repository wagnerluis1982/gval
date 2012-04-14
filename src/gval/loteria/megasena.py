# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import MegaSenaParser

class MegaSena(Loteria):
    _parser_class = MegaSenaParser
    _posicao_numeros = xrange(28, 34)
