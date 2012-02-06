# -*- coding: utf-8 -*-
from test_stuff.util import (ServidorDownload, PAGINAS, CONTEUDO_ASCII,
                             CONTEUDO_ENCODING)

from should_dsl import should, should_not
from lib.gval.util import Downloader

class TestDownloader:
    @classmethod
    def setUpClass(cls):
        cls.servidor = ServidorDownload()
        cls.servidor.iniciar()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.finalizar()

    def test_download_conteudo(self):
        "#download deve retornar o '<conteúdo>' da url"
        download = Downloader().download
        url = self.servidor.url + PAGINAS['ASCII']

        download(url) |should| equal_to(CONTEUDO_ASCII)

    def test_download_encoding(self):
        "#download deve retornar u'<unicode>' quando servidor envia encoding"
        download = Downloader().download
        pagina_iso = download(self.servidor.url + PAGINAS['ISO-8859-1'])
        pagina_utf = download(self.servidor.url + PAGINAS['UTF-8'])

        pagina_iso |should| be_instance_of(unicode)
        pagina_iso |should| equal_to(CONTEUDO_ENCODING % 'ISO-8859-1')

        pagina_utf |should| be_instance_of(unicode)
        pagina_utf |should| equal_to(CONTEUDO_ENCODING % 'UTF-8')

    def test_download_raw_string(self):
        "#download deve retornar '<str>' se encoding é desconhecido"
        download = Downloader().download
        url = self.servidor.url + PAGINAS['UNKNOWN']

        download(url) |should| be_instance_of(str)
