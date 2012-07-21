# language: pt-br

Funcionalidade: Apostador confere aposta
  Como um apostador da Loteria
  Eu quero conferir minha aposta
  Para que eu saiba se ganhei algum prêmio

  As loterias dão prêmios de acordo com a seguinte tabela:
    | loteria   | acertos      |
    | Lotofácil | 11 a 15      |
    | Lotomania | 16 a 20 ou 0 |
    | Quina     | 03 a 05      |
    | Mega Sena | 04 a 06      |

  Esquema do Cenário: conferência da Lotofácil
    Dado que eu apostei no jogo da Lotofácil
    E que eu apostei no concurso <n>
    E que eu apostei nos números "<numeros>"
    Quando eu confiro essa aposta
    Então eu devo saber que acertei <q> acertos
    E eu devo saber que acertei os números "<acertados>"
    E eu devo saber que eu ganhei <premio>

    Exemplos:
      | n   | numeros                                      | q  | acertados                                 | premio  |
      | 600 | 02 04 05 06 07 09 10 11 15 17 18 19 20 21 24 | 8  | 05 06 09 10 11 17 18 19                   | 0.00    |
      | 659 | 01 02 04 05 07 08 09 10 11 13 15 19 20 22 24 | 11 | 01 04 05 08 09 10 11 15 19 20 24          | 2.50    |
      | 700 | 01 02 06 07 08 09 10 13 14 16 18 19 21 22 24 | 14 | 01 02 06 07 08 09 10 13 14 16 18 19 21 22 | 2543.83 |

  Esquema do Cenário: conferência da Lotomania
    Dado que eu apostei no jogo da Lotomania
    E que eu apostei no concurso <n>
    E que eu apostei nos números "<numeros>"
    Quando eu confiro essa aposta
    Então eu devo saber que acertei <q> acertos
    E eu devo saber que acertei os números "<acertados>"
    E eu devo saber que eu ganhei <premio>

    Exemplos:
      | n    | numeros                                                     | q | acertados | premio    |
      | 914  | 00 03 04 05 06 07 08 10 12 13 14 17 18 19 20 21 22 23 24 25 | 0 |           | 104985.56 |
      | 1112 | 01 02 04 06 07 08 09 10 11 12 13 14 15 16 17 18 20 21 22 23 | 1 | 01        | 0.00      |

  Esquema do Cenário: conferência da Quina
    Dado que eu apostei no jogo da Quina
    E que eu apostei no concurso <n>
    E que eu apostei nos números "<numeros>"
    Quando eu confiro essa aposta
    Então eu devo saber que acertei <q> acertos
    E eu devo saber que acertei os números "<acertados>"
    E eu devo saber que eu ganhei <premio>

    Exemplos:
      | n    | numeros        | q | acertados      | premio    |
      | 805  | 13 23 45 47 78 | 1 | 13             | 0.00      |
      | 1763 | 03 09 24 33 60 | 5 | 03 09 24 33 60 | 143758.75 |
      | 2811 | 16 19 59 63 76 | 3 | 16 19 59       | 109.68    |

  Esquema do Cenário: conferência da Mega Sena
    Dado que eu apostei no jogo da Mega Sena
    E que eu apostei no concurso <n>
    E que eu apostei nos números "<numeros>"
    Quando eu confiro essa aposta
    Então eu devo saber que acertei <q> acertos
    E eu devo saber que acertei os números "<acertados>"
    E eu devo saber que eu ganhei <premio>

    Exemplos:
      | n    | numeros           | q | acertados   | premio |
      | 1379 | 05 12 36 45 51 55 | 4 | 05 12 36 45 | 399.06 |
