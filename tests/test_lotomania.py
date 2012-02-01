import test_stuff.urls

from should_dsl import should, should_not
from lib.gval.loteria import Lotomania

class TestLotomania:
    URL = test_stuff.urls.URLS['lotomania']

    def test_consultar(self):
        consultar = lambda n: Lotomania(concurso=n,
                                    url=self.URL % n).consultar()

        consultar(914) |should| equal_to(dict(
            concurso=914,
            numeros=[1,2,9,11,15,16,27,32,39,52,57,59,63,64,69,73,75,76,78,93]
          ))
