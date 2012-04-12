# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import QuinaParser

class Quina(Loteria):
    def _extrair_resultado(self, html):
        parser = QuinaParser()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=0,
            numeros=range(21, 26)
        )

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
