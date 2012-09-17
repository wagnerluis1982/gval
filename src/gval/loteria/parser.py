from HTMLParser import HTMLParser


class LoteriaParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        setattr(self.__class__, 'dados', property(self.__class__.obter_dados))

    def obter_dados(self):
        return ''.join(self._dados).split('|')

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


class LotofacilParser(LoteriaParser):
    pass


class LotomaniaParser(LoteriaParser):
    pass


class QuinaParser(LoteriaParser):
    def reset(self):
        LoteriaParser.reset(self)

        self._capturar_lista = False
        self._capturar_numero = False
        self._numeros = []

    def handle_starttag(self, tag, attrs):
        LoteriaParser.handle_starttag(self, tag, attrs)

        if tag == "li":
            self._capturar_numero = True

        if tag == "ul":
            self._capturar_lista = True

    def handle_endtag(self, tag):
        LoteriaParser.handle_endtag(self, tag)

        if tag == "li":
            self._capturar_numero = False

        if tag == "ul" and self._capturar_lista and len(self._numeros) > 0:
            self._dados.append('|' + '|'.join(self._numeros) + '|')
            self._numeros = []

    def handle_data(self, data):
        LoteriaParser.handle_data(self, data)

        if self._capturar_numero:
            self._numeros.append(data)


class MegaSenaParser(QuinaParser):
    pass
