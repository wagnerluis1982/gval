# -*- coding: utf-8 -*-
import codecs
import cookielib
import errno
import os
import re
import sys
import urllib2

# TODO: tornar portável
def home_cachedir():
    if sys.platform.startswith('linux'):
        env_home = os.environ.get('HOME')

        if env_home:
            subdirs = ('.gval', 'cache', 'paginas')
            cachedir = os.path.join(env_home, os.sep.join(subdirs))

            try:
                os.makedirs(cachedir)
            except OSError, e:
                EXISTE = e.errno == errno.EEXIST
                if not EXISTE or (EXISTE and not os.access(cachedir, os.W_OK)):
                    return None

            return cachedir

class Cacher(object):
    def __init__(self, cachedir):
        self._cachedir = cachedir

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
