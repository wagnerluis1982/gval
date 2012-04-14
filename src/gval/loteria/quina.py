# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import QuinaParser

class Quina(Loteria):
    _parser_class = QuinaParser
    _posicao_numeros = xrange(21, 26)
