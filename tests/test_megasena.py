import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import MegaSena
from lib.gval.util import Config

class TestMegaSena:
    "MegaSena"

    def test_consultar(self):
        "#consultar retorna dict(<resultado_megasena>)"

        cfg = Config(test_stuff.CONFIG_DIR)
        sena = MegaSena(cfg)

        sena.consultar(1379) |should| equal_to(dict(
            concurso=1379,
            numeros=[5, 12, 36, 45, 50, 58]
          ))
