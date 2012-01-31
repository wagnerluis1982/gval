# language: pt-br

Funcionalidade: Apostador consulta resultado
  Como um apostador da Loteria
  Eu informo o jogo e o número do concurso
  Para que eu saiba qual foi o resultado

  Esquema do Cenário: resultados da Lotofácil
    Dado que eu apostei no jogo da Lotofácil
    E que eu apostei no concurso <n>
    Quando eu consulto o resultado dessa aposta
    Então eu devo obter os números "<resultado>"

    Exemplos:
      | n   | resultado                                    |
      | 600 | 01 03 05 06 08 09 10 11 16 17 18 19 22 23 25 |
      | 659 | 01 03 04 05 06 08 09 10 11 12 15 19 20 23 24 |
      | 700 | 01 02 06 07 08 09 10 13 14 16 18 19 21 22 25 |

  Esquema do Cenário: resultados da Lotomania
    Dado que eu apostei no jogo da Lotomania
    E que eu apostei no concurso <n>
    Quando eu consulto o resultado dessa aposta
    Então eu devo obter os números "<resultado>"

    Exemplos:
      | n    | resultado                                                   |
      | 914  | 01 02 09 11 15 16 27 32 39 52 57 59 63 64 69 73 75 76 78 93 |
      | 1112 | 01 03 05 19 24 25 28 33 41 47 54 56 70 75 78 87 91 92 95 96 |
      | 1208 | 07 08 09 11 32 45 46 49 51 58 60 71 73 77 89 92 93 95 96 99 |
