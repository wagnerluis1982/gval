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

        return list( set(a).intersection(b) )

class ConfigException(Exception):
    pass

class Config(object):
    def __init__(self, config_dir=None):
        # Atributo de instância
        self._cache_dir = None

        # Usa o diretório passado se não nulo
        if config_dir is not None:
            self._config_dir = config_dir

        # Define o diretório de configuração de acordo com o SO
        # Por enquanto é suportado os sistemas Posix e Windows (NT)
        else:
            if os.name == 'posix':
                prefixo = '.'
                profile_dir = os.environ.get("HOME")

            elif os.name == 'nt':
                prefixo = '_'
                profile_dir = os.environ.get("APPDATA")

            # Se nenhum SO for detectado, lança uma exceção
            else:
                raise ConfigException("Impossível de detectar local do "
                                      "diretório de configuração.")

            self._config_dir = os.path.join(profile_dir,
                                            "{0}gval".format(prefixo))

    def get_config_dir(self, *subdirs):
        cfg_dir = os.path.join(self._config_dir, *subdirs)
        self.makedirs(cfg_dir)
        return cfg_dir
    config_dir = property(fget=get_config_dir)

    def get_cache_dir(self, *subdirs):
        self._cache_dir = self._cache_dir or os.path.join(self._config_dir,
                                                          'cache')
        return self.get_config_dir(self._cache_dir, *subdirs)
    cache_dir = property(fget=get_cache_dir)

    def makedirs(self, caminho):
        """Versão própria do makedirs()

        Essa versão não lança exceção se o caminho já existir
        """
        try:
            os.makedirs(caminho)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

class Cacher(object):
    def __init__(self, cfg):
        self._cachedir = cfg.get_cache_dir('paginas')

    def _secure_path(self, name):
        return os.path.join(self._cachedir, re.sub('[:/]', '_', name))

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
