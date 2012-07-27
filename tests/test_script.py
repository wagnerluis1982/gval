# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.util import Config
from lib.gval.script import Script

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

    def test_preparar__consultar(self):
        "#preparar cmd consultar retorna (<method>, ('<jogo>', <num>))"

        args = 'consultar', '--jogo', 'lotofacil', '--concurso', '600'
        esperado = (self.script.consultar, ('lotofacil', 600))
        self.script.preparar(*args) |should| equal_to(esperado)

        args = 'consultar', '--jogo=megasena', '--concurso', '605'
        esperado = (self.script.consultar, ('megasena', 605))
        self.script.preparar(*args) |should| equal_to(esperado)

        args = 'consultar', '--concurso=610', '--jogo', 'quina'
        esperado = (self.script.consultar, ('quina', 610))
        self.script.preparar(*args) |should| equal_to(esperado)

        args = 'consultar', '-j', 'lotomania', '-c', '600' # opção curta
        esperado = (self.script.consultar, ('lotomania', 600))
        self.script.preparar(*args) |should| equal_to(esperado)

    def test_preparar__conferir(self):
        "#preparar cmd conferir retorna (<method>, ('<jogo>', <num>, <aposta>))"

        args = 'conferir', '--jogo', 'lotofacil', '--concurso', '600',  \
                    '--aposta', '01 02 03 04 05 06 07 08 09 10 11 12 13 14 15'
        esperado = (self.script.conferir, ('lotofacil', 600,
                    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)))
        self.script.preparar(*args) |should| equal_to(esperado)

    def test_gval_consultar(self):
        "#gval-consultar deve retornar o resultado da loteria solicitada"

        fmt = SaidaFormatter(
            "Consulta de Resultado\n"
            "---------------------\n"
            "* Loteria: %s\n"
            "* Concurso: %d\n"
            "* Números: %s\n"
        )

        self.script.consultar('lotofacil', '600') |should| equal_to(0)

        saida_esperada = fmt.gerar('Lotofacil', 600,
                                '01 03 05 06 08 09 10 11 16 17 18 19 22 23 25')
        self.saida.readlines() |should| equal_to(saida_esperada)
