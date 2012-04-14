# -*- coding: utf-8 -*-
import test_stuff

from lettuce import *
from should_dsl import should, should_not
from lib.gval.loteria import *
from lib.gval.util import Config
Given = When = Then = step

@Given(u'^Dado que eu apostei no jogo da Lotofácil$')
def dado_jogo_lotofacil(step):
    world.jogo = "lotofacil"

@Given(u'^Dado que eu apostei no jogo da Lotomania$')
def dado_jogo_lotomania(step):
    world.jogo = "lotomania"

@Given(u'^Dado que eu apostei no jogo da Quina$')
def dado_jogo_quina(step):
    world.jogo = "quina"

@Given(u'^Dado que eu apostei no jogo da Mega Sena$')
def dado_jogo_megasena(step):
    world.jogo = "megasena"

@Given(u'^E que eu apostei no concurso (\d+)$')
def dado_concurso(step, concurso):
    world.concurso = int(concurso)

@When(u'^Quando eu consulto o resultado dessa aposta$')
def quando_consulta_resultado(step):
    classes_loteria = {
        'lotofacil': Lotofacil,
        'lotomania': Lotomania,
        'quina': Quina,
    }
    cfg = Config(config_dir=test_stuff.CONFIG_DIR)
    instancia = classes_loteria[world.jogo](cfg)

    world.resultado = instancia.consultar(world.concurso)['numeros']

@Then(u'^Então eu devo obter os números "([^"]*)"$')
def entao_obter_numeros(step, resultado):
    numeros = map(int, resultado.split())
    world.resultado |should| equal_to(numeros)
