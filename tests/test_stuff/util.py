# -*- coding: utf-8 -*-
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import os.path
import threading

# Pasta em que se encontram os arquivos que devem ser servidos pelo servidor
DATA_DIR = os.path.join(os.path.dirname(__file__), 'util_data')

# Nome das páginas armazenadas
PAGINAS = {
    "UNKNOWN": "pagina_unknown.html",
    "ASCII": "pagina_ascii.html",
    "ISO-8859-1": "pagina_iso_8859_1.html",
    "UTF-8": "pagina_utf8.html",
}


# As strings abaixo são para serem usadas nos testes da função download

CONTEUDO_ASCII = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="ASCII" />
        <title>Teste de gval.util</title>
    </head>
    <body>
        <h1>Teste</h1>
        <p>
            Fim do Teste
        </p>
    </body>
</html>
"""

CONTEUDO_ENCODING = u"""<!DOCTYPE html>
<html>
    <head>
        <meta charset="%s" />
        <title>Teste de gval.util</title>
    </head>
    <body>
        <h1>Teste cõm encódîngs</h1>
        <p>
            Fím do Testé
        </p>
    </body>
</html>
"""

class ServidorDownload:
    # Implementação de servidor http simples, que retorna o charset correto para
    # os arquivos de testes da função download_pagina.
    endereco = ('127.0.0.1', 15707)
    url = "http://%s:%s/" % endereco

    class RequestHandler(SimpleHTTPRequestHandler):
        # Essa subclasse é quem verdadeiramente realiza o serviço
        def log_message(self, *args, **kwargs):
            # Sobrescrevendo esse método para que não seja exibida mensagens de
            # log no terminal.
            pass

        def guess_type(self, path):
            charset = {PAGINAS['ISO-8859-1']: 'ISO-8859-1',
                       PAGINAS['UTF-8']: 'UTF-8',
                }.get(os.path.basename(self.translate_path(path)))

            if not charset:
                return SimpleHTTPRequestHandler.guess_type(self, path)

            return "text/html; charset=%s" % charset

    def iniciar(self):
        os.chdir(DATA_DIR)

        self.servidor = HTTPServer(self.endereco, self.RequestHandler)
        t = threading.Thread(target=self.servidor.serve_forever)
        t.start()

    def finalizar(self):
        self.servidor.shutdown()
        self.servidor.server_close()
