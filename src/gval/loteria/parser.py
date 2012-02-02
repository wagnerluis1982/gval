from HTMLParser import HTMLParser

class LoteriaParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        setattr(self.__class__, 'dados', property(self.__class__.obter_dados))

    def obter_dados(self):
        return ''.join(self._dados)

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

class QuinaParser(LoteriaParser):
    def obter_dados(self):
        dados = LoteriaParser.obter_dados(self)

        return dados.format(sorteados='|'.join(self._numeros))

    def reset(self):
        LoteriaParser.reset(self)

        self._span_id2 = False
        self._capturar_numero = False
        self._numeros = []

    def handle_starttag(self, tag, attrs):
        LoteriaParser.handle_starttag(self, tag, attrs)

        if self._span_id2 and tag == "li":
            self._capturar_numero = True

        if tag == "span" and ("id", "sorteio2") in attrs:
            self._span_id2 = True
            self._dados.append("{sorteados}")

    def handle_endtag(self, tag):
        LoteriaParser.handle_endtag(self, tag)

        if self._span_id2 and tag == "li":
            self._capturar_numero = False

        if self._span_id2 and tag == "span":
            self._span_id2 = False

    def handle_data(self, data):
        LoteriaParser.handle_data(self, data)

        if self._capturar_numero:
            self._numeros.append(data)
