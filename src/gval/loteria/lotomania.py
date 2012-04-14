# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LotomaniaParser

class Lotomania(Loteria):
    _url_script = ("_lotomania_pesquisa.asp")

    def _extrair_resultado(self, html):
        parser = LotomaniaParser()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=0,
            numeros=range(6, 26)
        )

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
