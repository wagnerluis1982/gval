from HTMLParser import HTMLParser

class LoteriaParser(HTMLParser):
    def obter_dados(self):
        return ''.join(self._dados)
    dados = property(obter_dados)

    def reset(self):
        HTMLParser.reset(self)

        self._capturar = True
        self._dados = []

    def handle_starttag(self, tag, attrs):
        self._capturar = False

    def handle_endtag(self, tag):
        self._capturar = True

    def handle_data(self, data):
        if self._capturar:
            self._dados.append(data)

    def feed(self, data):
        HTMLParser.feed(self, data)
