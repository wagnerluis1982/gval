# -*- coding: utf-8 -*-
import test_stuff.util

from should_dsl import should, should_not
from lib.gval.util import *
from nose import SkipTest

class TestUtil_download_pagina:
    "Util #download_pagina"

    @classmethod
    def setUpClass(cls):
        cls.servidor = test_stuff.util.ServidorDownloadPagina()
        cls.servidor.iniciar()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.finalizar()

    def test_download_pagina_conteudo(self):
        "retorna o '<conteúdo>' da url"
        url = '/'.join((self.servidor.url, test_stuff.util.PAGINAS['ASCII']))

        download_pagina(url) |should| equal_to(test_stuff.util.CONTEUDO_ASCII)

    def test_download_pagina_encoding(self):
        "retorna u'<unicode>' quando servidor envia encoding"
        url = '/'.join((self.servidor.url, test_stuff.util.PAGINAS['ISO-8859-1']))
        pagina = download_pagina(url)

        pagina |should| be_instance_of(unicode)
        pagina |should| equal_to(test_stuff.util.CONTEUDO_UNICODE)

    def test_download_pagina_raw_string(self):
        "retorna '<string>' se encoding é desconhecido"
        url = '/'.join((self.servidor.url, test_stuff.util.PAGINAS['UNKNOWN']))
        pagina = download_pagina(url)

        pagina |should| be_instance_of(str)
