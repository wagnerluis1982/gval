# -*- coding: utf-8 -*-
import re

from gval import download_pagina
from gval.loteria import Loteria
from gval.loteria.parser import LoteriaParser

class Lotofacil(Loteria):
    _loteria = 'lotofacil'

    def consultar(self):
        self.html = self.html or download_pagina(self.url)
        
        return self._extrair_resultado(self.html)

    def _extrair_resultado(self, html):
        dados = LoteriaParser().feed(html)

        pattern = (r"(\d+)\|+"           # concurso
                   r"((?:\d{2}\|){15})") # numeros sorteados
        matched = re.match(pattern, dados).groups()

        return {'concurso': int(matched[0]),
                'numeros': self._numeros(matched[1])}

    def _numeros(self, match):
        # quebra match por '|', retornando uma lista numérica
        return [int(num) for num in match.split('|') if num]
