# language: pt-br

Funcionalidade: Apostador consulta resultado
  Como um apostador
  Eu informo o jogo e o número do concurso
  Para que eu saiba qual foi o resultado

  Esquema do Cenário: consulta resultado
    Dado que eu apostei no jogo da "<loteria>"
    E que eu apostei no concurso <n>
    Quando eu consulto o resultado dessa aposta
    Então eu devo obter os números "<resultado>"

    Exemplos:
      | loteria   | n   | resultado                                    |
      | lotofacil | 600 | 01 03 05 06 08 09 10 11 16 17 18 19 22 23 25 |
      | lotofacil | 659 | 01 03 04 05 06 08 09 10 11 12 15 19 20 23 24 |
      | lotofacil | 700 | 01 02 06 07 08 09 10 13 14 16 18 19 21 22 25 |
