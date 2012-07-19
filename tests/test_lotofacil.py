# -*- coding: utf-8 -*-
import test_stuff

from should_dsl import should, should_not
from lib.gval.loteria import Lotofacil, Resultado, Conferencia, Aposta
from lib.gval.util import Config

class TestLotofacil:
    def __init__(self):
        cfg = Config(test_stuff.CONFIG_DIR)
        self.lotofacil = Lotofacil(cfg)

    def test_consultar(self):
        "#consultar retorna Resultado(<lotofacil>)"

        lotofacil = self.lotofacil

        lotofacil.consultar(600) |should| equal_to(Resultado(
            concurso=600,
            numeros=[1,3,5,6,8,9,10,11,16,17,18,19,22,23,25]
          ))
        lotofacil.consultar(659) |should| equal_to(Resultado(
            concurso=659,
            numeros=[1,3,4,5,6,8,9,10,11,12,15,19,20,23,24]
          ))

    def test_conferir(self):
        "#conferir retorna os acertos e valor do prêmio de uma aposta"

        lotofacil = self.lotofacil

        aposta = Aposta(600, [2,4,5,6,7,9,10,11,15,17,18,19,20,21,24])
        conferido = lotofacil.conferir(aposta)
        esperado = Conferencia(aposta,
                               resultado=lotofacil.consultar(600), # chamando função com teste próprio
                               quantidade=8,
                               acertados=[5, 6, 9, 10, 11, 17, 18, 19],
                               premio=0.00)

        conferido |should| equal_to(esperado)
