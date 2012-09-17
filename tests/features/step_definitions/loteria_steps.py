# -*- coding: utf-8 -*-
import test_stuff

from lettuce import *
from should_dsl import should, should_not
from lib.gval.loteria import *
from lib.gval.util import Config
Given = When = Then = step


@before.all
def setup_all():
    world.cfg = Config(test_stuff.CONFIG_DIR)


@Given(u'^Dado que eu apostei no jogo da Lotofácil$')
def dado_jogo_lotofacil(step):
    world.jogo = Loteria("lotofacil", world.cfg)


@Given(u'^Dado que eu apostei no jogo da Lotomania$')
def dado_jogo_lotomania(step):
    world.jogo = Loteria("lotomania", world.cfg)


@Given(u'^Dado que eu apostei no jogo da Quina$')
def dado_jogo_quina(step):
    world.jogo = Loteria("quina", world.cfg)


@Given(u'^Dado que eu apostei no jogo da Mega Sena$')
def dado_jogo_megasena(step):
    world.jogo = Loteria("megasena", world.cfg)


@Given(u'^E que eu apostei no concurso (\d+)$')
def dado_concurso(step, concurso):
    world.concurso = int(concurso)
