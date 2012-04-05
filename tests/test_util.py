# -*- coding: utf-8 -*-
from test_stuff.util import (ServidorDownload,
                             DiretorioTemporario,
                             PAGINAS,
                             CONTEUDO_ASCII,
                             CONTEUDO_ENCODING)

from should_dsl import should, should_not
from lib.gval.util import Downloader, Cacher
import os

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

class TestCacher:
    @classmethod
    def setUpClass(cls):
        cls._dirtemp = DiretorioTemporario()
        cls.dirtemp = str(cls._dirtemp)
        cls.cacher = Cacher(cls.dirtemp)

        cls.arquivo = "arquivo_em_cache"
        cls.caminho = os.path.join(cls.dirtemp, cls.arquivo)
        cls.conteudo = 100 * "Um texto repetido 100 vezes "

    @classmethod
    def tearDownClass(cls):
        del cls._dirtemp

    def test_guardar_em_cache(self):
        "#guardar deve armazenar um arquivo em cache"
        guardar = self.cacher.guardar

        guardar(self.arquivo, self.conteudo)
        os.path.exists(self.caminho) |should| be(True)

        # A função também pode ser chamada com os nomes dos argumentos
        guardar(filename=self.arquivo+'1', content=self.conteudo)
        os.path.exists(self.caminho+'1') |should| be(True)

    def test_obter_do_cache(self):
        "#obter deve retornar o conteúdo de um arquivo em cache"
        self.cacher.obter(self.arquivo) |should| equal_to(self.conteudo)

    def test_obter_nao_cache(self):
        "#obter deve retornar None para arquivos que não estejam em cache"
        self.cacher.obter(self.arquivo+'9') |should| be(None)
