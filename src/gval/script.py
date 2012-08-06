# -*- coding: utf-8 -*-
import gval.loteria
import gval.util
import argparse
import sys

LOTERIAS = {
   'lotofacil': gval.loteria.Lotofacil,
   'lotomania': gval.loteria.Lotomania,
   'quina': gval.loteria.Quina,
   'megasena': gval.loteria.MegaSena,
}

class ScriptException(Exception):
    pass

class T(object):
    """Classe de tipos para serem usadas com argparse

    Cada método representa um type para ArgParse.add_argument. Os métodos
    escritos aqui são sempre staticmethod ou classmethod.
    """
    @staticmethod
    def aposta(valores):
        numeros = tuple(map(int, valores.split()))
        return numeros

    @staticmethod
    def jogo(nome):
        if LOTERIAS.has_key(nome):
            return nome

        msg = ("\n"
               "    O jogo '%s' não existe ou ainda não foi implementado\n"
               "    IMPLEMENTADOS: {%s}")
        loterias = ", ".join(sorted(LOTERIAS.keys()))
        raise argparse.ArgumentTypeError(msg % (nome, loterias))

class Script(object):
    def __init__(self, saida=None, cfg=None):
        self.saida = saida or sys.stdout
        self.cfg = cfg or gval.util.Config()

    def cmd_consultar(self, loteria, concurso):
        saida = self.saida

        klass = LOTERIAS[loteria]
        try:
            result = klass().consultar(concurso)
            assert isinstance(result, gval.loteria.Resultado)

            saida.write(''.join(self.formatar_resultado(klass.__name__,
                                                        result.concurso,
                                                        result.numeros)))
        except ValueError:
            msg = "concurso %d da %s não encontrado"
            psr_consultar.error(msg % (concurso, loteria))

        return 0

    def cmd_conferir(self):
        pass

    def executar(self, *argv):
        avaliacao = self.avaliar(*argv)
        avaliacao[0](*avaliacao[1])

    def avaliar(self, *argv):
        global parser
        parser = argparse.ArgumentParser(prog=argv[0])
        subparsers = parser.add_subparsers(dest="comando")

        # Argumentos comuns para "jogo"
        args_jogo = ("-j", "--jogo")
        kwargs_jogo = {"help": "nome da loteria", "required": True,
                       "type": T.jogo}

        # Argumentos comuns para "concurso"
        args_concurso = ("-c", "--concurso")
        kwargs_concurso = {"help": "número do concurso", "required": True,
                           "type": int}

        # Comando "consultar"
        global psr_consultar
        psr_consultar = subparsers.add_parser("consultar")
        psr_consultar.add_argument(*args_jogo, **kwargs_jogo)
        psr_consultar.add_argument(*args_concurso, **kwargs_concurso)

        # Comando "conferir"
        global psr_conferir
        psr_conferir = subparsers.add_parser("conferir")
        psr_conferir.add_argument(*args_jogo, **kwargs_jogo)
        psr_conferir.add_argument(*args_concurso, action="append",
                                  **kwargs_concurso)
        psr_conferir.add_argument("-a", "--aposta", required=True,
                                  help=("aposta para conferir "
                                        "(ex: '01 07 11 13 29')"),
                                  action="append", type=T.aposta)

        # Análise das informações
        args = parser.parse_args(argv[1:])

        ret_method = getattr(self, "cmd_%s" % args.comando)
        ret_args = [args.jogo, args.concurso]

        if args.comando == "conferir":
            ret_args.append(args.aposta)

        return (ret_method, tuple(ret_args))

    def formatar_resultado(self, loteria, concurso, resultado):
        cabecalho = "Resultado da %s %d\n" % (loteria, concurso)

        return [cabecalho,
                '-' * (len(cabecalho) - 1) + '\n',
                "Números: %s\n" % ' '.join("%02d" % n for n in resultado)]
