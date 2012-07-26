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
