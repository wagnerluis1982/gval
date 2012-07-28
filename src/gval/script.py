# -*- coding: utf-8 -*-
import gval.loteria
import gval.util
import sys
import getopt

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

    def preparar(self, *argv):
        # Opções comuns
        opcoes_curtas = ["j:"]
        opcoes_longas = ["jogo="]

        # Comando para executar
        comando = argv[0]

        # Tenta achar o método do comando enviado. Caso o método não seja
        # encontrado, é lançada uma exceção.
        try:
            ret_method = getattr(self, "cmd_%s" % comando)
        except AttributeError:
            raise ScriptException("Comando não encontrado")

        # Opções por comando
        if comando in ("consultar", "conferir"):
            opcoes_curtas.append("c:")
            opcoes_longas.append("concurso=")

            if comando == "conferir":
                opcoes_curtas.append("a:")
                opcoes_longas.append("aposta=")

        # Processamento das opções
        opts, args = getopt.getopt(argv[1:], ''.join(opcoes_curtas), opcoes_longas)

        jogo = None
        concursos = []
        apostas = []
        for option, arg in opts:
            if option in ("-j", "--jogo"):
                jogo = arg
            elif option in ("-c", "--concurso"):
                concursos.append( int(arg) )
            elif option in ("-a", "--aposta"):
                apostas.append( tuple( map(int, arg.split()) ) )

        # Argumentos do método
        ret_args = [jogo]
        if comando == "consultar":
            ret_args.append(concursos[-1]) # último concurso passado em argv
        else: # comando conferir
            ret_args.extend([concursos, apostas])

        return (ret_method, tuple(ret_args))
