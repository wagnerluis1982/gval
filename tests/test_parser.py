# -*- coding: utf-8 -*-
from should_dsl import should, should_not
from lib.gval.loteria.parser import *


class TestLoteriaParser:
    "LoteriaParser"

    def test_obter_dados(self):
        "#obter_dados retorna ['texto fora das tags']"

        html = ("texto<b>que está <i>entre</i></b> <hide>tags ou</hide>"
                "fora das tags")
        parser = LoteriaParser()
        parser.feed(html)

        parser.dados |should| equal_to(["texto fora das tags"])


class TestQuinaParser:
    "QuinaParser"

    def test_obter_dados(self):
        "#obter_dados retorna ['texto fora ', '01', '02', '03', '04', ' texto fora']"

        html = ('texto fora '
            '<ul><li>01</li><li>02</li><li>03</li><li>04</li></ul>'
            ' texto fora')
        parser = QuinaParser()
        parser.feed(html)

        parser.dados |should| equal_to(["texto fora ", "01", "02",
                                        "03", "04", " texto fora"])
