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

def cache_filename(string):
    return re.sub('[:/]', '_', string)

def download_pagina(url, cache_dir=None):
    page_data = None
    cache = not url.startswith('file:') and bool(cache_dir)

    if cache:
        # Substitue as barras da url por um valor permitido para nomes de
        # arquivo para formar o nome para o arquivo de cache
        cache_file = os.path.join(cache_dir, cache_filename(url))

        # Obtém os dados do cache, se houver
        try:
            f = codecs.open(cache_file, 'r', encoding='utf-8')
        except IOError:
            pass
        else:
            page_data = f.read()
            f.close()

            # Se já obteve o cache, não é preciso gravar de novo em cache
            cache = False

    # Acessa a Internet, caso o arquivo não esteja em cache
    if not page_data:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders.append(("Cookie", "security=true"))

        page = opener.open(url)
        page_data = page.read()
        charset = page.headers.getparam('charset')

        if charset:
            try:
                page_data = unicode(page_data, charset)
            except (UnicodeDecodeError, LookupError):
                pass

    if cache:
        f = codecs.open(cache_file, 'w', encoding='utf-8')
        f.write(page_data)
        f.close()

    return page_data

# Novas implementações #

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
