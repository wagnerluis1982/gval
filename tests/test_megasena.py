import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import MegaSena, Resultado
from lib.gval.util import Config

class TestMegaSena:
    "MegaSena"

    def test_consultar(self):
        "#consultar retorna Resultado(<megasena>)"

        cfg = Config(test_stuff.CONFIG_DIR)
        sena = MegaSena(cfg)

        r = sena.consultar(1379)
        r.concurso |should| equal_to(1379)
        r.numeros |should| equal_to([5, 12, 36, 45, 50, 58])
