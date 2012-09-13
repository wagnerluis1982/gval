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
    def __init__(self, out=None, cfg=None):
        self.out = out or sys.stdout
        self.cfg = cfg or gval.util.Config()

    def cmd_consultar(self, loteria, concurso):
        klass = LOTERIAS[loteria]
        try:
            result = klass().consultar(concurso)
            assert isinstance(result, gval.loteria.Resultado)

            self.out.write(''.join(self.formatar_resultado(klass.__name__,
                                                        result.concurso,
                                                        result.numeros)))
        except gval.loteria.LoteriaException:
            msg = u"concurso %d da %s não encontrado"
            psr_consultar.error(msg % (concurso, loteria))

        return 0

    def cmd_conferir(self, loteria, concursos, numeros):
        klass = LOTERIAS[loteria]
        lote = klass()
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

        self.out.write(''.join(self.formatar_conferencia(klass.__name__,
                                                      conferidos)))
        # TODO: Melhorar as informações de erros
        if erros:
            self.out.write(u"Concursos não disponíveis: %s\n" % list(erros))

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

    def formatar_resultado(self, loteria, concurso, resultado):
        return [u"Resultado da %s %d\n" % (loteria, concurso),
                u"  Números: %s\n" % ' '.join("%02d" % n for n in resultado)]

    def formatar_conferencia(self, loteria, dados):
        concursos = sorted(set(d[0] for d in dados))
        primeiro = concursos[0]
        ultimo   = concursos[-1]

        s_concursos = [str(num) for num in concursos]
        if len(concursos) > 2:
            if concursos == range(primeiro, ultimo + 1):
                txt_concursos = "%d a %d" % (primeiro, ultimo)
            else:
                txt_concursos = ", ".join(s_concursos[:-1]) + " e %d" % ultimo
        else:
            txt_concursos = " e ".join(s_concursos)

        premiadas = [p for p in dados if p[3] > 0]
        premiacao = locale.format("%.2f", sum(v[3] for v in premiadas),
                                  grouping=True)

        msg_premiadas = (u"  %d aposta{0} premiada{0}"
                         u" (em %d conferida{1})\n").format('s' * (len(premiadas) > 1),
                                                            's' * (len(dados) > 1))

        return [u"Conferência da %s %s\n" % (loteria, txt_concursos),
                msg_premiadas % (len(premiadas), len(dados)),
                u"  Premiação total: R$ %s\n" % premiacao]


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
