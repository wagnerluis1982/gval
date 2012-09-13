# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.util import Config
from lib.gval import script
import unittest
import os
from UserList import UserList

class Output(UserList):
    def write(self, message):
        assert isinstance(message, basestring)
        self.data.extend(message.splitlines(True))

    def clear(self):
        self.data = []

class TestScript:
    def setUp(self):
        self.out = Output()
        self.script = script.Script(out=self.out,
                                    err=open(os.devnull),
                                    cfg=Config(test_stuff.CONFIG_DIR))

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
        "#avaliar comando conferir retorna (<method>, ('<jogo>', [<num>,...], [<aposta>,...]))"

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

        (lambda: s.avaliar('gval.py', 'latir')) |should| throw(script.ScriptException)
        (lambda: s.avaliar('gval.py', 'miar')) |should| throw(script.ScriptException)
        (lambda: s.avaliar('gval.py', 'falar')) |should| throw(script.ScriptException)

    def test_script__consultar(self):
        "gval.py consultar -j <loteria> -c <num>"

        error_code = self.script.cmd_consultar('quina', 805)
        error_code |should| equal_to(0)
        self.out |should| contain(u"Resultado da Quina 805\n")
        self.out |should| contain(u"  Números: 13 22 41 42 71\n")

    def test_script__conferir__simples(self):
        "gval.py conferir -j <loteria> -c <num> -a <aposta>"

        error_code = self.script.cmd_conferir('quina', [805],
                                              [(13, 23, 41, 71, 78)])
        error_code |should| equal_to(0)
        self.out |should| contain(u"Conferência da Quina 805\n")
        self.out |should| contain(u"  1 aposta premiada (em 1 conferida)\n")
        self.out |should| contain(u"  Premiação total: R$ 33,13\n")

    def test_script__conferir__2_concursos(self):
        "gval.py conferir -j <loteria> -c <num> -c <num> -a <aposta>"

        error_code = self.script.cmd_conferir('quina', [805, 807],
                                              [(13, 23, 41, 71, 78)])
        error_code |should| equal_to(0)
        self.out |should| contain(u"Conferência da Quina 805 e 807\n")
        self.out |should| contain(u"  1 aposta premiada (em 2 conferidas)\n")
        self.out |should| contain(u"  Premiação total: R$ 33,13\n")
