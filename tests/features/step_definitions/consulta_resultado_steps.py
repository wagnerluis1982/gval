# -*- coding: utf-8 -*-
from loteria_steps import *

@When(u'^Quando eu consulto o resultado dessa aposta$')
def quando_consulta_resultado(step):
    world.resultado = world.instancia().consultar(world.concurso)['numeros']

@Then(u'^Então eu devo obter os números "([^"]*)"$')
def entao_obter_numeros(step, resultado):
    resultado = map(int, resultado.split())
    world.resultado |should| equal_to(resultado)
