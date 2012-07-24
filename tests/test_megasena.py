# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import MegaSena, Aposta, Conferencia
from lib.gval.util import Config

class TestMegaSena:
    "MegaSena"

    cfg = Config(test_stuff.CONFIG_DIR)

    def setUp(self):
        self.sena = MegaSena(self.cfg)

    def test_consultar(self):
        "#consultar retorna Resultado(<megasena>)"

        r = self.sena.consultar(1379)
        r.concurso |should| equal_to(1379)
        r.numeros |should| equal_to([5, 12, 36, 45, 50, 58])

    def test_conferir(self):
        "#conferir retorna os acertos e valor do prêmio de uma aposta"

        sena = self.sena

        aposta = Aposta(1379, [5, 12, 36, 45, 51, 55])
        conferido = sena.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=sena.consultar(aposta.concurso), # chamando função com teste próprio
                        quantidade=4,
                        acertados=[5, 12, 36, 45],
                        premio=399.06)
        conferido |should| equal_to(esperado)
