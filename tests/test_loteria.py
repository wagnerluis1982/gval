# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Conferencia, Resultado, Aposta, Loteria
from lib.gval.util import Config

cfg = Config(test_stuff.CONFIG_DIR)


class TestLoteria:
    def test_consultar__quina(self):
        "#consultar retorna Resultado(<quina>)"

        quina = Loteria("quina", cfg)
        r = quina.consultar(805)
        r.concurso |should| equal_to(805)
        r.numeros |should| equal_to([13, 22, 41, 42, 71])

    def test_conferir__quina(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Quina"

        quina = Loteria("quina", cfg)

        aposta = Aposta(805, [13, 23, 45, 47, 78])
        conferido = quina.conferir(aposta)
        conferido.quantidade |should| equal_to(1)
        conferido.acertados |should| equal_to([13])
        conferido.premio |should| equal_to(0.00)

        aposta = Aposta(1763, [3, 9, 24, 33, 60])
        conferido = quina.conferir(aposta)
        conferido.quantidade |should| equal_to(5)
        conferido.acertados |should| equal_to([3, 9, 24, 33, 60])
        conferido.premio |should| equal_to(143758.75)

    def test_consultar__megasena(self):
        "#consultar retorna Resultado(<megasena>)"

        sena = Loteria("megasena", cfg)
        r = sena.consultar(1379)
        r.concurso |should| equal_to(1379)
        r.numeros |should| equal_to([5, 12, 36, 45, 50, 58])

    def test_conferir__megasena(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Mega Sena"

        sena = Loteria("megasena", cfg)

        aposta = Aposta(1379, [5, 12, 36, 45, 51, 55])
        conferido = sena.conferir(aposta)
        conferido.quantidade |should| equal_to(4)
        conferido.acertados |should| equal_to([5, 12, 36, 45])
        conferido.premio |should| equal_to(399.06)

    def test_consultar__lotofacil(self):
        "#consultar retorna Resultado(<lotofacil>)"

        lotofacil = Loteria("lotofacil", cfg)

        r = lotofacil.consultar(600)
        r.concurso |should| equal_to(600)
        r.numeros |should| equal_to([1,3,5,6,8,9,10,11,16,17,18,19,22,23,25])

        r = lotofacil.consultar(659)
        r.concurso |should| equal_to(659)
        r.numeros |should| equal_to([1,3,4,5,6,8,9,10,11,12,15,19,20,23,24])

    def test_conferir__lotofacil(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Lotofácil"

        lotofacil = Loteria("lotofacil", cfg)

        aposta = Aposta(600, [2,4,5,6,7,9,10,11,15,17,18,19,20,21,24])
        conferido = lotofacil.conferir(aposta)
        conferido.quantidade |should| equal_to(8)
        conferido.acertados |should| equal_to([5, 6, 9, 10, 11, 17, 18, 19])
        conferido.premio |should| equal_to(0.00)

        aposta = Aposta(659, [1,2,4,5,7,8,9,10,11,13,15,19,20,22,24])
        conferido = lotofacil.conferir(aposta)
        conferido.quantidade |should| equal_to(11)
        conferido.acertados |should| equal_to([1,4,5,8,9,10,11,15,19,20,24])
        conferido.premio |should| equal_to(2.50)

    def test_consultar__lotomania(self):
        "#consultar retorna Resultado(<lotomania>)"

        lotomania = Loteria("lotomania", cfg)
        r = lotomania.consultar(914)
        r.concurso |should| equal_to(914)
        r.numeros |should| equal_to([1, 2, 9, 11, 15, 16, 27, 32, 39, 52, 57,
                                     59, 63, 64, 69, 73, 75, 76, 78, 93])

    def test_conferir(self):
        "#conferir retorna os acertos e o prêmio de uma aposta da Lotomania"

        lotomania = Loteria("lotomania", cfg)

        aposta = Aposta(1112, [1,2,4,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23])
        conferido = lotomania.conferir(aposta)
        conferido.quantidade |should| equal_to(1)
        conferido.acertados |should| equal_to([1])
        conferido.premio |should| equal_to(0.00)

        aposta = Aposta(914, [0,3,4,5,6,7,8,10,12,13,14,17,18,19,20,21,22,23,24,25])
        conferido = lotomania.conferir(aposta)
        conferido.quantidade |should| equal_to(0)
        conferido.acertados |should| equal_to([])
        conferido.premio |should| equal_to(104985.56)


class TestConferencia:
    def test_acertos_premio(self):
        "verifica os acertos e premiacao"

        aposta = Aposta(805, [13, 23, 41, 47, 71])
        resultado = Loteria("quina", cfg).consultar(805)
        confere = Conferencia(aposta, resultado)

        confere.acertados |should| equal_to([13, 41, 71])
        confere.quantidade |should| equal_to(3)
        confere.premio |should| equal_to(33.13)

    def test_runtimeerror_concursos_diferentes(self):
        "lança RuntimeError se os concursos são diferentes"

        aposta = Aposta(805, [13, 23, 41, 47, 71])
        resultado = Resultado(900, [17, 26, 34, 52, 77])
        confere = lambda: Conferencia(aposta, resultado)

        confere |should| throw(RuntimeError)
