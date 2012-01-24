import test_stuff.urls

from should_dsl import should, should_not
from lib.gval.loteria import *

class TestLotofacil:
    URL = test_stuff.urls.URLS['lotofacil']

    def test_consultar(self):
        "Lotofacil #consultar"
        loteria = Lotofacil()
        lotofacil = lambda n: loteria.consultar(n, self.URL % n)['numeros']

        lotofacil(600) |should| equal_to([1,3,5,6,8,9,10,11,16,17,18,19,22,23,25])
        lotofacil(659) |should| equal_to([1,3,4,5,6,8,9,10,11,12,15,19,20,23,24])
