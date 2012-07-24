# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Lotofacil, Conferencia, Aposta
from lib.gval.util import Config

class TestLotofacil:
    cfg = Config(test_stuff.CONFIG_DIR)

    def setUp(self):
        self.lotofacil = Lotofacil(self.cfg)

    def test_consultar(self):
        "#consultar retorna Resultado(<lotofacil>)"

        r = self.lotofacil.consultar(600)
        r.concurso |should| equal_to(600)
        r.numeros |should| equal_to([1,3,5,6,8,9,10,11,16,17,18,19,22,23,25])

        r = self.lotofacil.consultar(659)
        r.concurso |should| equal_to(659)
        r.numeros |should| equal_to([1,3,4,5,6,8,9,10,11,12,15,19,20,23,24])

    def test_conferir(self):
        "#conferir retorna os acertos e valor do prêmio de uma aposta"

        lotofacil = self.lotofacil

        aposta = Aposta(600, [2,4,5,6,7,9,10,11,15,17,18,19,20,21,24])
        conferido = lotofacil.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=lotofacil.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=8,
                        acertados=[5, 6, 9, 10, 11, 17, 18, 19],
                        premio=0.00)
        conferido |should| equal_to(esperado)

        aposta = Aposta(659, [1,2,4,5,7,8,9,10,11,13,15,19,20,22,24])
        conferido = lotofacil.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=lotofacil.consultar(aposta.concurso),
                        quantidade=11,
                        acertados=[1,4,5,8,9,10,11,15,19,20,24],
                        premio=2.50)
        conferido |should| equal_to(esperado)
