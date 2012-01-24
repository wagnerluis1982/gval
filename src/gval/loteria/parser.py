from HTMLParser import HTMLParser

class LoteriaParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)

        self.capturar = True
        self.dados = []

    def handle_starttag(self, tag, attrs):
        self.capturar = False

    def handle_endtag(self, tag):
        self.capturar = True

    def handle_data(self, data):
        if self.capturar:
            self.dados.append(data)

    def feed(self, data):
        HTMLParser.feed(self, data)
        return ''.join(self.dados)
