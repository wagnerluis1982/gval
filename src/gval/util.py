# -*- coding: utf-8 -*-
import codecs
import cookielib
import errno
import os
import re
import urllib2


class Util(object):
    @staticmethod
    def intersecao(a, b):
        assert isinstance(a, (list, tuple, set))
        assert isinstance(b, (list, tuple, set))

        return sorted(set(a).intersection(b))

    @staticmethod
    def maketrans_unicode(frm, to, to_none=True):
        assert isinstance(frm, basestring)
        assert isinstance(to, basestring)

        length = len(frm)
        if len(to) != length:
            raise ValueError("os argumentos devem ter o mesmo comprimento")

        if to_none:
            _ord = (lambda c: ord(c) if c != '\0' else None)
        else:
            _ord = ord

        table = {}
        for i in xrange(length):
            table[_ord(frm[i])] = _ord(to[i])

        return table

    @staticmethod
    def str_to_numeral(str_numero, xtype=float):
        if isinstance(str_numero, str):
            str_numero = str_numero.decode("utf8")
        elif not isinstance(str_numero, unicode):
            raise TypeError("str_numero deve ser str ou unicode")

        tabela = Util.maketrans_unicode(",.", ".\0")

        return xtype(str_numero.translate(tabela))


class ConfigException(Exception):
    pass


class Config(object):
    def __init__(self, config_dir=None):
        # Diretório de config vem do parâmetro passado ou do padrão do sistema
        self._cfg_dir = config_dir or self._default_dir()

        # Diretório de cache. Definido ao usar get_cache_dir
        self._cache_dir = None

    def _default_dir(self):
        # Define o diretório de configuração de acordo com o SO
        # Por enquanto é suportado os sistemas Posix e Windows (NT)
        if os.name == 'posix':
            prefixo = '.'
            profile_dir = os.environ.get("HOME")

        elif os.name == 'nt':
            prefixo = '_'
            profile_dir = os.environ.get("APPDATA")

        # Se nenhum SO for detectado, lança uma exceção
        else:
            raise ConfigException("Impossível detectar caminho do diretório de"
                                  "configuração.")

        return os.path.join(profile_dir, prefixo + "gval")

    def get_config_dir(self, *subdirs):
        cfg_dir = os.path.join(self._cfg_dir, *subdirs)
        self.makedirs(cfg_dir)

        return cfg_dir

    def get_cache_dir(self, *subdirs):
        if self._cache_dir is None:
            self._cache_dir = self.get_config_dir("cache", *subdirs)

        return self._cache_dir

    def makedirs(self, caminho):
        """Versão própria do makedirs()

        Essa versão não lança exceção se o caminho já existir
        """
        try:
            os.makedirs(caminho)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    config_dir = property(get_config_dir)
    cache_dir = property(get_cache_dir)


class Cacher(object):
    def __init__(self, cfg):
        self._cache_dir = cfg.get_cache_dir('paginas')

    def _secure_path(self, name):
        return os.path.join(self._cache_dir, re.sub('[:/?]', '_', name))

    def guardar(self, filename, content):
        # Grava os dados no arquivo
        f = codecs.open(self._secure_path(filename), 'w', encoding='utf-8')
        f.write(content)
        f.close()

    def obter(self, filename):
        # Caminho com nome seguro
        caminho = self._secure_path(filename)

        content = None
        try:
            f = codecs.open(caminho, 'r', encoding='utf-8')
        except IOError:
            pass
        else:
            content = f.read()
            f.close()

        return content


class Downloader(object):
    def download(self, url):
        # As páginas de resultado das Loterias exigem cookies
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        # Foi percebido que a adição desse cookie dobrou o tempo de resposta
        opener.addheaders.append(("Cookie", "security=true"))

        page = opener.open(url)
        page_data = page.read()
        charset = page.headers.getparam('charset')

        if charset is not None:
            try:
                page_data = unicode(page_data, charset)
            except (UnicodeDecodeError, LookupError):
                pass

        return page_data
