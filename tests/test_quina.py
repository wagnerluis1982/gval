import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Quina, Resultado
from lib.gval.util import Config

class TestQuina:
    def test_consultar(self):
        "#consultar retorna Resultado(<quina>)"

        cfg = Config(test_stuff.CONFIG_DIR)
        quina = Quina(cfg)

        quina.consultar(805) |should| equal_to(Resultado(
            concurso=805,
            numeros=[13, 22, 41, 42, 71]
          ))
