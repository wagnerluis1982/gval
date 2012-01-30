# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LoteriaParser

class Lotofacil(Loteria):
    _loteria = 'lotofacil'

    def _extrair_resultado(self, html):
        parser = LoteriaParser()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=0,
            numeros=range(3, 18)
        )

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
