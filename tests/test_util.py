# -*- coding: utf-8 -*-
from test_stuff.util import (ServidorDownload,
                             DiretorioTemporario,
                             PAGINAS,
                             CONTEUDO_ASCII,
                             CONTEUDO_ENCODING)

from should_dsl import should, should_not
from lib.gval.util import Config, Downloader, Cacher, Util
import os

class TestConfig:
    def setUp(self):
        self._dirtemp = DiretorioTemporario()
        self.cfg = Config(str(self._dirtemp))

    def tearDown(self):
        del self._dirtemp

    def test_get_config_dir(self):
        "#get_config_dir deve retornar um caminho válido"
        os.path.exists(self.cfg.config_dir) |should| be(True)

    def test_get_cache_dir(self):
        "#get_cache_dir deve retornar um caminho válido"
        os.path.exists(self.cfg.cache_dir) |should| be(True)

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
        cfg = Config(str(cls._dirtemp))
        cls.cacher = Cacher(cfg)

        cls.arquivo = "arquivo_em_cache"
        cls.caminho = os.path.join(cfg.get_cache_dir('paginas'), cls.arquivo)
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

class TestUtil:
    def test_intersecao(self):
        "#intersecao retorna list(<itens em comum>)"

        Util.intersecao([1,2,3,4,5], [4,5,6,7,8]) |should| equal_to([4,5])

        # teste com parâmetro tuple
        Util.intersecao((1,2,3,4,5), [4,5,6,7,8]) |should| equal_to([4,5])

        # teste com parâmetro set
        Util.intersecao([1,2,3,4,5], set([4,5,6,7,8])) |should| equal_to([4,5])

    def test_str_to_numeral__tfloat(self):
        "#str_to_numeral converte u'198.678,07' => float(198678.07)"

        Util.str_to_numeral(u'198.678,07') |should| equal_to(198678.07)

    def test_str_to_numeral__tint(self):
        "#str_to_numeral converte u'167.465' => int(167465)"

        Util.str_to_numeral(u'167.465') |should| equal_to(167465)

    def test_str_to_numeral__error(self):
        "#str_to_numeral lança TypeError se o argumento não é string"

        (lambda: Util.str_to_numeral(6578)) |should| throw(TypeError)
