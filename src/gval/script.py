# -*- coding: utf-8 -*-
import gval.loteria
import gval.util
import argparse
import sys

ERRO_NOARGS = 1
ERRO_EXISTE = 2
ERRO_ENCONT = 3

CLASSES = {
   'lotofacil': gval.loteria.Lotofacil,
   'lotomania': gval.loteria.Lotomania,
   'quina': gval.loteria.Quina,
   'megasena': gval.loteria.MegaSena,
}

class ScriptException(Exception):
    pass

class Script(object):
    def __init__(self, saida=None, cfg=None):
        self.saida = saida or sys.stdout
        self.cfg = cfg or gval.util.Config()

    def cmd_consultar(self, *args):
        saida = self.saida

        if len(args) < 1:
            saida.write("ERRO: Número de argumentos inválido\n")
            saida.write("Modo de uso: gval-consultar <loteria> [concurso]\n")
            return ERRO_NOARGS

        loteria = args[0]
        concurso = len(args) > 1 and int(args[1]) or None

        try:
            klass = CLASSES[loteria]
        except KeyError:
            saida.write("ERRO: a loteria '%s' não existe ou ainda não foi "
                        "implementada\n" % loteria)
            saida.write("IMPLEMENTADAS: %s\n" % ', '.join(CLASSES.keys()))
            return ERRO_EXISTE
        else:
            try:
                resultado = klass().consultar(concurso)

                saida.write("Consulta de Resultado\n")
                saida.write("---------------------\n")
                saida.write("* Loteria: %s\n" % klass.__name__)
                saida.write("* Concurso: %d\n" % resultado.concurso)
                saida.write("* Números: %s\n" % ' '.join(["%02d" % n for n in
                                                        resultado.numeros]))
            except ValueError:
                saida.write("ERRO: Concurso n. %d da %s não encontrado\n" %
                                                    (concurso, klass.__name__))
                return ERRO_ENCONT

        return 0

    def cmd_conferir(self):
        pass

    def executar(self, *argv):
        avaliacao = self.avaliar(*argv)
        avaliacao[0](*avaliacao)

    def avaliar(self, *argv):
        parser = argparse.ArgumentParser(prog=argv[0])
        subparsers = parser.add_subparsers(dest="comando")

        # Argumentos comuns para "jogo"
        args_jogo = ("-j", "--jogo")
        kwargs_jogo = {"help": "Nome da loteria", "required": True}

        # Argumentos comuns para "concurso"
        args_concurso = ("-c", "--concurso")
        kwargs_concurso = {"help": "Número do concurso", "required": True,
                           "type": int}

        # Comando "consultar"
        psr_consultar = subparsers.add_parser("consultar")
        psr_consultar.add_argument(*args_jogo, **kwargs_jogo)
        psr_consultar.add_argument(*args_concurso, **kwargs_concurso)

        # Comando "conferir"
        psr_conferir = subparsers.add_parser("conferir")
        psr_conferir.add_argument(*args_jogo, **kwargs_jogo)
        psr_conferir.add_argument(*args_concurso, action="append",
                                  **kwargs_concurso)
        psr_conferir.add_argument("-a", "--aposta", required=True,
                                  help=("Aposta para conferir. "
                                        "Ex: 01 07 11 13 29"),
                                  action="append")

        # Análise das informações
        args = parser.parse_args(argv[1:])

        ret_method = getattr(self, "cmd_%s" % args.comando)
        ret_args = [args.jogo, args.concurso]

        if args.comando == "conferir":
            apostas = [tuple(map(int, a.split())) for a in args.aposta]
            ret_args.append(apostas)

        return (ret_method, tuple(ret_args))

    def formatar_resultado(self, loteria, concurso, resultado):
        cabecalho = "Resultado da %s %d\n" % (loteria, concurso)

        return [cabecalho,
                '-' * (len(cabecalho) - 1) + '\n',
                "Números: %s\n" % ' '.join("%02d" % n for n in resultado)]
