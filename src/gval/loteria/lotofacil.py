# -*- coding: utf-8 -*-
import re

from gval import download_pagina
from gval.loteria import Loteria
from gval.loteria.parser import LoteriaParser

class Lotofacil(Loteria):
    def consultar(self, concurso, url=None):
        url = url or self._url_consulta('lotofacil', concurso)
        html = download_pagina(url)
        
        return self._extrair_resultado(html)

    def _extrair_resultado(self, html):
        dados = LoteriaParser().feed(html)

        pattern = (r"(\d+)\|+"           # concurso
                   r"((?:\d{2}\|){15})") # numeros sorteados
        matched = re.match(pattern, dados).groups()

        return {'concurso': matched[0],
                'numeros': self._numeros(matched[1])}

    def _numeros(self, match):
        # quebra match por '|', retornando uma lista numérica
        return [int(num) for num in match.split('|') if num]
