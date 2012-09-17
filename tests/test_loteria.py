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

    def test_consultar__lotofacil(self):
        "#consultar retorna Resultado(<lotofacil>)"

        lotofacil = Loteria(self.cfg, nome="lotofacil")

        r = lotofacil.consultar(600)
        r.concurso |should| equal_to(600)
        r.numeros |should| equal_to([1,3,5,6,8,9,10,11,16,17,18,19,22,23,25])

        r = lotofacil.consultar(659)
        r.concurso |should| equal_to(659)
        r.numeros |should| equal_to([1,3,4,5,6,8,9,10,11,12,15,19,20,23,24])

    def test_conferir__lotofacil(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Lotofácil"

        lotofacil = Loteria(self.cfg, nome="lotofacil")

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
