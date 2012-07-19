# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Conferencia, Resultado, Aposta
from lib.gval.util import Config

class TestConferencia:
    def setUp(self):
        self.conferencia = Conferencia()

    def test_calcula_acertos(self):
        "#calcula_acertos verifica os números acertados e a quantidade destes"

        c = self.conferencia

        c.aposta = Aposta(805, [13, 23, 45, 47, 78])
        c.resultado = Resultado(805, [13, 22, 41, 42, 71])
        c.calcula_acertos()

        c.acertados |should| equal_to([13])
        c.quantidade |should| equal_to(1)
