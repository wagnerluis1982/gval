# -*- coding: utf-8 -*-
from gval import download_pagina
from gval.loteria import Loteria
from gval.loteria.parser import LoteriaParser

class Lotofacil(Loteria):
    _loteria = 'lotofacil'

    def consultar(self):
        self.html = self.html or download_pagina(self.url)

        return self._extrair_resultado(self.html)

    def _extrair_resultado(self, html):
        parser = LoteriaParser()
        parser.feed(html)

        POSICAO = dict(
            concurso=0,
            numeros=range(3, 18)
        )

        resultado = parser.dados.split('|')

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
