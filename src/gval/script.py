# -*- coding: utf-8 -*-
import gval.loteria
import gval.util
import argparse
import sys
import locale

locale.setlocale(locale.LC_NUMERIC, "")

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

        msg = (u"\n"
               u"    O jogo '%s' não existe ou ainda não foi implementado\n"
               u"    IMPLEMENTADOS: {%s}")
        loterias = ", ".join(sorted(LOTERIAS.keys()))
        raise argparse.ArgumentTypeError(msg % (nome, loterias))

class Script(object):
    def __init__(self, out=sys.stdout, err=sys.stderr, cfg=None):
        self.out = out
        self.err = err
        self.cfg = cfg

    def _msg_lista(self, numeros):
        assert isinstance(numeros, list)

        numeros = sorted(set(numeros))
        primeiro = numeros[0]
        ultimo   = numeros[-1]

        str_numeros = lambda: [str(num) for num in numeros]
        if len(numeros) > 2:
            if numeros == range(primeiro, ultimo + 1):
                return "%d a %d" % (primeiro, ultimo)
            else:
                return ", ".join(str_numeros()[:-1]) + " e %d" % ultimo
        else:
            return " e ".join(str_numeros())

    def cmd_consultar(self, loteria, concurso):
        klass = LOTERIAS[loteria]

        try:
            result = klass(self.cfg).consultar(concurso)
            assert isinstance(result, gval.loteria.Resultado)

            self.out.write(u"Resultado da %s %d\n" % (klass.__name__,
                                                      result.concurso))

            resultado = ' '.join("%02d" % n for n in result.numeros)
            self.out.write(u"  Números: %s\n" % resultado)

        except gval.loteria.LoteriaException:
            msg = u"concurso %d da %s não encontrado"
            psr_consultar.error(msg % (concurso, loteria))

        return 0

    def cmd_conferir(self, loteria, concursos, numeros):
        klass = LOTERIAS[loteria]
        lote = klass(self.cfg)

        apostas = [gval.loteria.Aposta(c, n) for c in concursos
                                             for n in numeros]
        conferidos = []
        erros = set()
        for apo in apostas:
            try:
                confere = lote.conferir(apo)
                assert isinstance(confere, gval.loteria.Conferencia)

                conferidos.append(confere.to_array())

            except gval.loteria.LoteriaException:
                erros.add(apo.concurso)

        if erros:
            self.err.write(u"ATENÇÃO: concursos indisponíveis: %s\n\n" %
                                                self._msg_lista(list(erros)))

        self.out.write(u"Conferência da %s %s\n" % (klass.__name__,
                                self._msg_lista([n[0] for n in conferidos])))

        premiadas = [p for p in conferidos if p[3] > 0]
        msg_premiadas = (u"  %d aposta{0} premiada{0} (em %d conferida{1})\n"
                            .format('s' * (len(premiadas) > 1),
                                    's' * (len(conferidos) > 1)))
        self.out.write(msg_premiadas % (len(premiadas), len(conferidos)))

        premiacao = locale.format("%.2f", sum(v[3] for v in premiadas),
                                    grouping=True)
        self.out.write(u"  Premiação total: R$ %s\n" % premiacao)

        return 0

    def executar(self, *argv):
        avaliacao = self.avaliar(*argv)
        avaliacao[0](*avaliacao[1])

    def avaliar(self, *argv):
        global parser
        parser = argparse.ArgumentParser(prog=argv[0])
        subparsers = parser.add_subparsers(dest="comando")

        # Argumentos comuns para "jogo"
        args_jogo = ("-j", "--jogo")
        kwargs_jogo = {"help": u"nome da loteria", "required": True,
                       "type": T.jogo}

        # Argumentos comuns para "concurso"
        args_concurso = ("-c", "--concurso")
        kwargs_concurso = {"help": u"número do concurso", "required": True,
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
                                  help=(u"aposta para conferir "
                                        u"(ex: '01 07 11 13 29')"),
                                  action="append", type=T.aposta)

        # Análise das informações
        args = parser.parse_args(argv[1:])

        ret_method = getattr(self, "cmd_%s" % args.comando)
        ret_args = [args.jogo, args.concurso]

        if args.comando == "conferir":
            ret_args.append(args.aposta)

        return (ret_method, tuple(ret_args))


def main(args=sys.argv):
    # As linhas abaixo mudam o nome do script se este estiver no path. Assim, um
    # script que esteja em /usr/bin por exemplo, vai ser exibido no help do GVAL
    # apenas como gval, não /usr/bin/gval.
    import os
    if os.path.dirname(args[0]) in sys.path:
        args[0] = os.path.basename(args[0])

    Script().executar(*args)

if __name__ == "__main__":
    main()
