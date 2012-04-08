# -*- coding: utf-8 -*-
import test_stuff

from lettuce import *
from should_dsl import should, should_not
from lib.gval.loteria import *
Given = When = Then = step

@Given(u'^Dado que eu apostei no jogo da Lotofácil$')
def dado_jogo(step):
    world.jogo = "lotofacil"

@Given(u'^Dado que eu apostei no jogo da Lotomania$')
def dado_jogo(step):
    world.jogo = "lotomania"

@Given(u'^Dado que eu apostei no jogo da Quina$')
def dado_jogo(step):
    world.jogo = "quina"

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
    instancia = classes_loteria[world.jogo](cache_dir=test_stuff.CACHE_DIR)

    world.resultado = instancia.consultar(world.concurso)['numeros']

@Then(u'^Então eu devo obter os números "([^"]*)"$')
def entao_obter_numeros(step, resultado):
    numeros = map(int, resultado.split())
    world.resultado |should| equal_to(numeros)
