# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Quina, Aposta, Conferencia
from lib.gval.util import Config

class TestQuina:
    cfg = Config(test_stuff.CONFIG_DIR)

    def setUp(self):
        self.quina = Quina(self.cfg)

    def test_consultar(self):
        "#consultar retorna Resultado(<quina>)"

        r = self.quina.consultar(805)
        r.concurso |should| equal_to(805)
        r.numeros |should| equal_to([13, 22, 41, 42, 71])

    def test_conferir(self):
        "#conferir retorna os acertos e valor do prêmio de uma aposta"

        quina = self.quina

        aposta = Aposta(805, [13, 23, 45, 47, 78])
        conferido = quina.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=quina.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=1,
                        acertados=[13],
                        premio=0.00)
        conferido |should| equal_to(esperado)

        aposta = Aposta(1763, [3, 9, 24, 33, 60])
        conferido = quina.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=quina.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=5,
                        acertados=[3, 9, 24, 33, 60],
                        premio=143758.75)
        conferido |should| equal_to(esperado)
