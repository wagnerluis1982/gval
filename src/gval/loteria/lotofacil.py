# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LotofacilParser

class Lotofacil(Loteria):
    _parser_class = LotofacilParser
    _posicao_numeros = xrange(3, 18)
