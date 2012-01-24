from should_dsl import should, should_not
from lib.gval.loteria.parser import *

class TestLoteriaParser:
    def test_feed(self):
        "LoteriaParser #feed"
        html = ("texto que <b>entre <i>tags</i></b>"
                "<hide>nao </hide>deve ser exibido")
        parser = LoteriaParser()

        parser.feed(html) |should| equal_to("texto que deve ser exibido")
