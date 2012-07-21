import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Quina, Resultado
from lib.gval.util import Config

class TestQuina:
    def test_consultar(self):
        "#consultar retorna Resultado(<quina>)"

        cfg = Config(test_stuff.CONFIG_DIR)
        quina = Quina(cfg)

        r = quina.consultar(805)
        r.concurso |should| equal_to(805)
        r.numeros |should| equal_to([13, 22, 41, 42, 71])
