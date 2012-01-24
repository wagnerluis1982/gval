import cookielib
import urllib2

def download_pagina(url):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page = opener.open(url)

    return page.read()
