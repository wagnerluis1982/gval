# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Conferencia, Resultado, Aposta, Loteria
from lib.gval.util import Config

class TestLoteria:
    cfg = Config(test_stuff.CONFIG_DIR)

    def test_consultar__quina(self):
        "#consultar retorna Resultado(<quina>)"

        quina = Loteria(self.cfg, nome="quina")
        r = quina.consultar(805)
        r.concurso |should| equal_to(805)
        r.numeros |should| equal_to([13, 22, 41, 42, 71])

    def test_conferir__quina(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Quina"

        quina = Loteria(self.cfg, nome="quina")

        aposta = Aposta(805, [13, 23, 45, 47, 78])
        conferido = quina.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=quina.consultar(aposta.concurso),
                        quantidade=1,
                        acertados=[13],
                        premio=0.00)
        conferido |should| equal_to(esperado)

        aposta = Aposta(1763, [3, 9, 24, 33, 60])
        conferido = quina.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=quina.consultar(aposta.concurso),
                        quantidade=5,
                        acertados=[3, 9, 24, 33, 60],
                        premio=143758.75)
        conferido |should| equal_to(esperado)

    def test_consultar__megasena(self):
        "#consultar retorna Resultado(<megasena>)"

        sena = Loteria(self.cfg, nome="megasena")
        r = sena.consultar(1379)
        r.concurso |should| equal_to(1379)
        r.numeros |should| equal_to([5, 12, 36, 45, 50, 58])

    def test_conferir__megasena(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Mega Sena"

        sena = Loteria(self.cfg, nome="megasena")

        aposta = Aposta(1379, [5, 12, 36, 45, 51, 55])
        conferido = sena.conferir(aposta)
        esperado = Conferencia(aposta,
                        resultado=sena.consultar(aposta.concurso),
                        quantidade=4,
                        acertados=[5, 12, 36, 45],
                        premio=399.06)
        conferido |should| equal_to(esperado)


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

    def test_calcula_acertos_erro_None(self):
        "#calcula_acertos lança RuntimeError se o resultado ou aposta é nulo"

        c = self.conferencia

        c.aposta = None
        c.resultado = Resultado(805, [13, 22, 41, 42, 71])
        c.calcula_acertos |should| throw(RuntimeError)

        c.aposta = Aposta(805, [13, 23, 45, 47, 78])
        c.resultado = None
        c.calcula_acertos |should| throw(RuntimeError)

        c.aposta = None
        c.resultado = None
        c.calcula_acertos |should| throw(RuntimeError)

    def test_calcula_acertos_erro_concurso(self):
        "#calcula_acertos lança RuntimeError se os concursos são diferentes"

        c = self.conferencia

        c.aposta = Aposta(805, [13, 23, 45, 47, 78])
        c.resultado = Resultado(900, [13, 22, 41, 42, 71])
        c.calcula_acertos |should| throw(RuntimeError)
