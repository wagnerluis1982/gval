import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Quina

class TestQuina:
    def test_consultar(self):
        "#consultar retorna dict(<resultado_quina>)"

        quina = Quina(cache_dir=test_stuff.CACHE_DIR)

        quina.consultar(805) |should| equal_to(dict(
            concurso=805,
            numeros=[13, 22, 41, 42, 71]
          ))
