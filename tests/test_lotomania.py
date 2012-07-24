# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Lotomania, Aposta, Conferencia
from lib.gval.util import Config

class TestLotomania:
    cfg = Config(test_stuff.CONFIG_DIR)

    def setUp(self):
        self.lotomania = Lotomania(self.cfg)

    def test_consultar(self):
        "#consultar retorna Resultado(<lotomania>)"

        r = self.lotomania.consultar(914)
        r.concurso |should| equal_to(914)
        r.numeros |should| equal_to([1,2,9,11,15,16,27,32,39,52,57,59,63,64,69,73,75,76,78,93])

    def test_conferir(self):
        "#conferir retorna os acertos e valor do prêmio de uma aposta"

        lotomania = self.lotomania

        aposta = Aposta(1112, [1,2,4,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23])
        conferido = lotomania.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=lotomania.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=1,
                        acertados=[1],
                        premio=0.00)
        conferido |should| equal_to(esperado)

        aposta = Aposta(914, [0,3,4,5,6,7,8,10,12,13,14,17,18,19,20,21,22,23,24,25])
        conferido = lotomania.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=lotomania.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=0,
                        acertados=[],
                        premio=104985.56)
        conferido |should| equal_to(esperado)
