# -*- coding: utf-8 -*-
from loteria_steps import *

@Given(u'^E que eu apostei nos números "([^"]*)"$')
def dado_numeros(step, numeros):
    world.numeros = map(int, numeros.split())

@When(u'^Quando eu confiro essa aposta$')
def quando_confiro_aposta(step):
    world.conferencia = world.instancia().conferir(world.concurso, world.numeros)

@Then(u'^Então eu devo saber que acertei (\d+) acertos$')
def devo_saber_quantidade_acertos(step, quantidade):
    quantidade = int(quantidade)
    world.conferencia.quantidade |should| equal_to(quantidade)

@Then(u'^E eu devo saber que acertei os números "([^"]*)"$')
def devo_saber_numeros_acertados(step, acertados):
    acertados = map(int, acertados.split())
    world.conferencia.acertados |should| equal_to(acertados)

@Then(u'^E eu devo saber que eu ganhei (\d+\.\d+)$')
def devo_saber_ganhei(step, premio):
    premio = float(premio)
    world.conferencia.premio |should| equal_to(premio)
