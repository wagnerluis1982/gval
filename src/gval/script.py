# -*- coding: utf-8 -*-
import gval.loteria
import gval.util
import argparse
import sys
import locale

locale.setlocale(locale.LC_NUMERIC, "")

LOTERIAS = ('lotofacil', 'lotomania', 'quina', 'megasena')

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
        if nome in LOTERIAS:
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

    def _seq_to_str(self, numbers):
        assert isinstance(numbers, (list, set, tuple))

        numbers = sorted(set(numbers))
        str_numbers = lambda: [str(num) for num in numbers]
        primeiro = numbers[0]
        ultimo   = numbers[-1]

        # No máximo 2 números
        if len(numbers) <= 2:
            return " e ".join(str_numbers())
        # Mais de 2 números
        else:
            # Sequência está dentro de uma faixa
            if numbers == range(primeiro, ultimo + 1):
                return "%d a %d" % (primeiro, ultimo)
            # Sequência não consecutiva
            else:
                return ", ".join(str_numbers()[:-1]) + " e %d" % ultimo

    def cmd_consultar(self, loteria, concurso):
        try:
            result = gval.loteria.Loteria(loteria, self.cfg).consultar(concurso)
            assert isinstance(result, gval.loteria.Resultado)

            self.out.write(u"Resultado da %s %d\n" % (loteria.title(),
                                                      result.concurso))

            resultado = ' '.join("%02d" % n for n in result.numeros)
            self.out.write(u"  Números: %s\n" % resultado)

        except gval.loteria.LoteriaException:
            msg = u"ERRO: resultado da %s %d indisponível\n"
            self.err.write(msg % (loteria.title(), concurso))
            return 1

        return 0

    def cmd_conferir(self, loteria, concursos, numeros):
        # Realiza a conferência, guarda o retorno em conferidos, quando sucesso
        # e guarda os que não foram possíveis conferir em erros.
        apostas = [gval.loteria.Aposta(c, n) for c in concursos for n in numeros]
        conferidos = []
        erros = set()
        for apo in apostas:
            try:
                confere = gval.loteria.Loteria(loteria, self.cfg).conferir(apo)
                assert isinstance(confere, gval.loteria.Conferencia)

                conferidos.append(confere.to_array())

            except gval.loteria.LoteriaException:
                erros.add(apo.concurso)

        msg_erro = "%s: concursos indisponíveis: %s\n"

        # Não encontrar nenhum dos concursos pedidos caracteriza como erro.
        # Assim, aqui uma mensagem de erro é exibida e o script é finalizado.
        q_conferidos = len(conferidos)
        if q_conferidos == 0:
            self.err.write(msg_erro % ("ERRO", self._seq_to_str(erros)))
            return 1

        # Informa ao usuário os concursos não disponíveis no momento
        if erros:
            self.err.write(msg_erro % ("AVISO", self._seq_to_str(erros)))
            self.err.write('\n')

        # Informa quais concursos foram conferidos
        self.out.write(u"Conferência da %s %s\n" % (loteria.title(),
                                self._seq_to_str([n[0] for n in conferidos])))

        # Exibe quantas apostas foram premiadas e quantas foram conferidas
        premiadas = [p[3] for p in conferidos if p[3] > 0]
        q_premiadas = len(premiadas)
        msg_premiada = {
                0: u"%s aposta premiada",   # singular
                1: u"%s apostas premiadas", # plural
            }[q_premiadas > 1] % (q_premiadas if q_premiadas > 0 else u"Nenhuma")
        msg_conferida = {
                0: u"(em %d conferida)",
                1: u"(em %d conferidas)",
            }[q_conferidos > 1] % q_conferidos
        self.out.write(u"  %s %s\n" % (msg_premiada, msg_conferida))

        # Exibe a premiação total do usuário
        premiacao = locale.format("%.2f", sum(premiadas), grouping=True)
        self.out.write(u"  Premiação total: R$ %s\n" % premiacao)

        return 0

    def executar(self, *argv):
        avaliacao = self.avaliar(*argv)
        exit(avaliacao[0](*avaliacao[1]))

    def avaliar(self, *argv):
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
        psr_consultar = subparsers.add_parser("consultar")
        psr_consultar.add_argument(*args_jogo, **kwargs_jogo)
        psr_consultar.add_argument(*args_concurso, **kwargs_concurso)

        # Comando "conferir"
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
