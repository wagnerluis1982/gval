import test_stuff.urls

from should_dsl import should, should_not
from lib.gval.loteria.lotofacil import *

class TestLotofacil:
    URL = test_stuff.urls.URLS['lotofacil']

    def test_consultar(self):
        consultar = lambda n: Lotofacil(concurso=n,
                                    url=self.URL % n).consultar()

        consultar(600) |should| equal_to(dict(
            concurso=600,
            numeros=[1,3,5,6,8,9,10,11,16,17,18,19,22,23,25]
          ))
        consultar(659) |should| equal_to(dict(
            concurso=659,
            numeros=[1,3,4,5,6,8,9,10,11,12,15,19,20,23,24]
          ))
