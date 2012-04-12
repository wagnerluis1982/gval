# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from gval.loteria.lotofacil import Lotofacil
from gval.util import Config
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

class TestScript:
    saida = Saida()

    @classmethod
    def setUpClass(cls):
        cls.script = Script(saida=cls.saida, cfg=Config(test_stuff.CONFIG_DIR))
        cls.formato_saida = (
            "Consulta de Resultado\n"
            "---------------------\n"
            "* Loteria: %s\n"
            "* Concurso: %d\n"
            "* Números: %s\n"
        )

    def setUp(self):
        self.saida.clear()

    def test_gval_consultar(self):
        "#gval-consultar deve retornar o resultado da loteria solicitada"

        self.script.consultar('lotofacil', '600') |should| equal_to(0)

        s = ('Lotofacil', 600, '01 03 05 06 08 09 10 11 16 17 18 19 22 23 25')
        saida_esperada = (self.formato_saida % s).splitlines(True)

        self.saida.readlines() |should| equal_to(saida_esperada)
