import cookielib
import urllib2

def download_pagina(url, charset=None):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(url)

    charset = charset or page.headers.getparam('charset')

    if charset:
        return unicode(page.read(), charset)
    else:
        return page.read()
