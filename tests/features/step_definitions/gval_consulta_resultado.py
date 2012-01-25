# -*- coding: utf-8 -*-
import test_stuff.urls

from lettuce import *
from should_dsl import should, should_not
from lib.gval.loteria.lotofacil import *
Given = When = Then = step

@Given(u'^Dado que eu apostei no jogo da "([^"]*)"$')
def dado_jogo(step, jogo):
    world.jogo = jogo

@Given(u'^E que eu apostei no concurso (\d+)$')
def dado_concurso(step, concurso):
    world.concurso = int(concurso)

@When(u'^Quando eu consulto o resultado dessa aposta$')
def quando_consulta_resultado(step):
    classes_loteria = {
        'lotofacil': Lotofacil
    }
    url = test_stuff.urls.URLS[world.jogo] % world.concurso
    instancia = classes_loteria[world.jogo](world.concurso, url)

    world.resultado = instancia.consultar()['numeros']

@Then(u'^Então eu devo obter os números "([^"]*)"$')
def entao_obter_numeros(step, resultado):
    numeros = map(int, resultado.split())
    world.resultado |should| equal_to(numeros)
