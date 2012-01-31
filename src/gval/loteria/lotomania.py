# -*- coding: utf-8 -*-
from gval.loteria import Loteria
from gval.loteria.parser import LoteriaParser

class Lotomania(Loteria):
    _loteria = 'lotomania'
    _url_loteria = ("{loteria}/_{loteria}_pesquisa.asp?submeteu=sim&opcao="
                    "concurso&txtConcurso={concurso}")

    def _extrair_resultado(self, html):
        parser = LoteriaParser()
        parser.feed(html)
        resultado = parser.dados.split('|')

        POSICAO = dict(
            concurso=0,
            numeros=range(6, 26)
        )

        return {'concurso': int(resultado[POSICAO['concurso']]),
                'numeros': [int(resultado[n]) for n in POSICAO['numeros']]}
