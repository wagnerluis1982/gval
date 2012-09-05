Gerador e Verificador de Apostas da Loteria
===========================================

ATENÇÃO
-------

Sistema em versão Alpha, nem todas as funcionalidades estão estáveis ou
disponíveis, bem como poderão haver mudanças na API.

Sobre
-----

O sistema GVAL surgiu com o propósito principal de conferir apostas feitas nas
Casas Lotéricas do Brasil.

Uma função secundária dele é de gerar números para as suas apostas. É o mesmo
que a surpresinha, mas aqui, você deve preencher os jogos manualmente.

Instalação
----------

Para instalar, basta baixar o projeto, descompactar e executar, no diretório
raiz

    $ python setup.py install

Ou, você pode executar diretamente

    $ pip install git+https://github.com/wagnerluis1982/gval

Uso
---

###Consultando um resultado

    $ gval.py consultar --jogo lotofacil --concurso 708
    Resultado da Lotofacil 708
      Números: 01 02 03 04 05 06 09 11 14 16 19 21 22 24 25

Para saber mais sobre o comando, digite:

    $ gval.py consultar --help

Futuramente, mais informações serão exibidas, como a premiação e os ganhadores
por estado/município.

###Conferindo apostas

Na conferência de resultados, é possível conferir mais de um concurso e apostas
de um tipo de jogo. No próximo exemplo é conferido apenas uma aposta.

    $ gval.py conferir --jogo quina --concurso 805 --aposta "13 22 42 55 59"
    Conferência da Quina 805
      1 apostas premiadas (em 1 conferidas)
      Premiação total: R$ 33,13

já no próximo, são conferidas duas apostas

    $ gval.py conferir --jogo quina --concurso 805 --concurso 806 --aposta "13 22 42 55 59"
    Conferência da Quina 805 e 806
      1 apostas premiadas (em 2 conferidas)
      Premiação total: R$ 33,13

Para a digitação ficar mais confortável, o comando oferece opções curtas. Assim,
o exemplo acima pode ser reescrito como

    gval.py conferir -j quina -c 805 -c 806 -a "13 22 42 55 59"

A conferência cruza os concursos e as apostas, de forma que que se for informado
3 concursos e 2 apostas, serão conferidas 6 apostas.

###Gerando números para aposta

Ainda não implementado
