Gerador e Verificador de Apostas da Loteria
===========================================

ATENÇÃO
-------

Sistema em versão Pré-Alpha, nem todas as funcionalidades estão disponíveis, bem
como pode haver mudanças na API.

Sobre
-----

O sistema GVAL surgiu com o propósito principal de conferir apostas feitas nas
Casas Lotéricas do Brasil.

Uma função secundária dele é de gerar números para as suas apostas. É o mesmo
que a surpresinha, mas aqui, você deve preencher os jogos.

Instalação
----------

Para instalar, basta baixar o projeto e executar, no diretório raiz

    python setup.py install

Ou, você pode executar diretamente

    pip install git+https://github.com/wagnerluis1982/gval

Uso
---

Por enquanto só está implementada a consulta de resultados. Para consultar um
resultado, a partir de um terminal, use o comando 'gval-consultar', que tem a
seguinte sintaxe:

    gval-consultar <loteria> <concurso>

Por exemplo, se quiser consultar o concurso 708 da Lotofácil, você irá digitar

    gval-consultar lotofacil 708

que será retornado:

    Consulta de Resultado
    ---------------------
    * Loteria: Lotofacil
    * Concurso: 708
    * Números: 01 02 03 04 05 06 09 11 14 16 19 21 22 24 25

Futuramente, mais informações serão exibidas, como a premiação e os ganhadores
por estado/município.
