# -*- coding: utf-8 -*-
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
            subdirs = ('.gval-cache', 'paginas')
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

def download_pagina(url, charset=None, cache_dir=home_cachedir()):
    page_data = None
    cache = not url.startswith('file:') and bool(cache_dir)

    if cache:
        # Substitue as barras da url por um valor permitido para nomes de
        # arquivo para formar o nome para o arquivo de cache
        cache_file = os.path.join(cache_dir, cache_filename(url))

        # Obtém os dados do cache, se houver
        try:
            f = open(cache_file, 'r')
        except IOError:
            pass
        else:
            page_data = f.read()
            f.close()

    if not page_data:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        page = opener.open(url)
        page_data = page.read()
        charset = charset or page.headers.getparam('charset')

    try:
        page_data = unicode(page_data, charset)
    except (UnicodeDecodeError, TypeError, LookupError):
        pass

    if cache:
        f = open(cache_file, 'w')
        f.write(page_data)
        f.close()

    return page_data
