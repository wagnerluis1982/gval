import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Lotofacil
from lib.gval.util import Config

class TestLotofacil:
    def test_consultar(self):
        "#consultar retorna dict(<resultado_lotofacil>)"

        cfg = Config(test_stuff.CONFIG_DIR)
        lotofacil = Lotofacil(cfg)

        lotofacil.consultar(600) |should| equal_to(dict(
            concurso=600,
            numeros=[1,3,5,6,8,9,10,11,16,17,18,19,22,23,25]
          ))
        lotofacil.consultar(659) |should| equal_to(dict(
            concurso=659,
            numeros=[1,3,4,5,6,8,9,10,11,12,15,19,20,23,24]
          ))
