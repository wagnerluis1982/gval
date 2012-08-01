# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.util import Config
from lib.gval.script import Script, ScriptException
import unittest

class Saida(file):
    def __init__(self):
        self.mensagem = []

    def readlines(self):
        return self.mensagem

    def write(self, msg):
        self.mensagem.append(msg)

    def clear(self):
        self.mensagem = []

class SaidaFormatter:
    def __init__(self, formato):
        self._formato = formato

    def gerar(self, *params):
        return (self._formato % params).splitlines(True)

class TestScript:
    def setUp(self):
        self.saida = Saida()
        self.script = Script(saida=self.saida, cfg=Config(test_stuff.CONFIG_DIR))

    def test_avaliar__consultar(self):
        "#avaliar comando consultar retorna (<method>, ('<jogo>', <num>))"

        # chamada mais comum
        args = 'gval.py', 'consultar', '--jogo', 'lotofacil', '--concurso', '600'
        esperado = (self.script.cmd_consultar, ('lotofacil', 600))
        self.script.avaliar(*args) |should| equal_to(esperado)

        # chamada com sinal de =
        args = 'gval.py', 'consultar', '--jogo=megasena', '--concurso', '605'
        esperado = (self.script.cmd_consultar, ('megasena', 605))
        self.script.avaliar(*args) |should| equal_to(esperado)

        # chamada em outra ordem
        args = 'gval.py', 'consultar', '--concurso=610', '--jogo', 'quina'
        esperado = (self.script.cmd_consultar, ('quina', 610))
        self.script.avaliar(*args) |should| equal_to(esperado)

        # chamada com opções curtas
        args = 'gval.py', 'consultar', '-j', 'lotomania', '-c', '600'
        esperado = (self.script.cmd_consultar, ('lotomania', 600))
        self.script.avaliar(*args) |should| equal_to(esperado)

    def test_avaliar__conferir(self):
        "#avaliar comando conferir retorna (<method>, ('<jogo>', <num>, <aposta>))"

        # 1 concurso e 1 aposta
        args = 'gval.py', 'conferir', '--jogo', 'lotofacil', \
                    '--concurso', '600', \
                    '--aposta', '01 02 03 04 05 06 07 08 09 10 11 12 13 14 15'
        esperado = (self.script.cmd_conferir, ('lotofacil', [600],
                    [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)]))
        self.script.avaliar(*args) |should| equal_to(esperado)

        # 1 concurso e 2 apostas
        args = 'gval.py', 'conferir', '--jogo', 'quina', '--concurso', '1345', \
                    '--aposta', '02 09 14 19 28', '--aposta', '23 33 41 44 49'
        esperado = (self.script.cmd_conferir, ('quina', [1345],
                    [(2, 9, 14, 19, 28), (23, 33, 41, 44, 49)]))
        self.script.avaliar(*args) |should| equal_to(esperado)

        # 2 concursos e 2 apostas
        args = 'gval.py', 'conferir', '--jogo', 'quina', '-c', '1345', \
                    '-c', '1346', '-a', '02 09 14 19 28', '-a', '23 33 41 44 49'
        esperado = (self.script.cmd_conferir, ('quina', [1345, 1346],
                    [(2, 9, 14, 19, 28), (23, 33, 41, 44, 49)]))
        self.script.avaliar(*args) |should| equal_to(esperado)

    def test_avaliar__erro(self):
        "#avaliar comando desconhecido lança ScriptException"

        raise unittest.SkipTest("Teste provavelmente obsoleto")

        s = self.script

        (lambda: s.avaliar('gval.py', 'latir')) |should| throw(ScriptException)
        (lambda: s.avaliar('gval.py', 'miar')) |should| throw(ScriptException)
        (lambda: s.avaliar('gval.py', 'falar')) |should| throw(ScriptException)

    def test_formatar_resultado(self):
        "#formatar_resultado retorna o resultado formatado"

        # O resultado formatado deve ficar +/- assim:

        #########################################
        ### Resultado da {loteria} {concurso} ###
        ### --------------------------------- ###
        ### Números: {resultado}              ###
        #########################################

        resultado = self.script.formatar_resultado("Quina", 805,
                                                   [13, 22, 41, 42, 71])
        resultado |should| contain("Resultado da Quina 805\n")
        resultado |should| contain("Números: 13 22 41 42 71\n")

    def test_gval_consultar(self):
        "#gval-consultar deve retornar o resultado da loteria solicitada"

        raise unittest.SkipTest("Interface em modificação")

        fmt = SaidaFormatter(
            "Consulta de Resultado\n"
            "---------------------\n"
            "* Loteria: %s\n"
            "* Concurso: %d\n"
            "* Números: %s\n"
        )

        self.script.cmd_consultar('lotofacil', '600') |should| equal_to(0)

        saida_esperada = fmt.gerar('Lotofacil', 600,
                                '01 03 05 06 08 09 10 11 16 17 18 19 22 23 25')
        self.saida.readlines() |should| equal_to(saida_esperada)
