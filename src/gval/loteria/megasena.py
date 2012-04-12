# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import MegaSenaParser

class MegaSena(Loteria):
    def _extrair_resultado(self, html):
        parser = MegaSenaParser()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=0,
            numeros=range(28, 34)
        )

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
