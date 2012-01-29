import cookielib
import urllib2

def download_pagina(url, charset=None):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(url)
    page_data = page.read()

    charset = charset or page.headers.getparam('charset')

    try:
        return unicode(page_data, charset)
    except (UnicodeDecodeError, TypeError, LookupError):
        return page_data
