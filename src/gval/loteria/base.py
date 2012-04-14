# -*- coding: utf-8 -*-
import gval.util
import os.path

class Loteria(object):
    # abstract class

    # Os atributos dessa classe servem para construir a url de acesso aos
    # resultados de cada loteria. Os valores inseridos aqui são os valores mais
    # comuns. Cada subclasse deve sobrescrever os valores dos atributos (exceto
    # da constante) para se adequar à url que deve ser usada

    # Url comum a todas as loterias conhecidas
    URL_BASE = "http://www1.caixa.gov.br/loterias/loterias/{loteria}"

    # Nome do script de acesso
    _url_script = "{loteria}_pesquisa_new.asp"

    # Parâmetros do script. Raramente muda
    _url_params = "?submeteu=sim&opcao=concurso&txtConcurso={concurso}"

    # String usada na marca {loteria}. Caso seja None, utiliza o nome da classe
    # com caixa reduzida
    _loteria = None

    def __init__(self, cfg=None):
        # Valores usados ao consultar() o resultado de um concurso
        self._loteria = self._loteria or self.__class__.__name__.lower()

        # Objeto responsável pelos downloads
        self.downloader = gval.util.Downloader()

        # Objeto responsável por gravar em cache
        cfg = cfg or gval.util.Config()
        self.cacher = gval.util.Cacher(cfg)

    def consultar(self, concurso):
        url = self.__url_consulta(concurso)

        content = self.cacher.obter(url)
        if content is None:
            content = self.downloader.download(url)
            self.cacher.guardar(url, content)

        return self._extrair_resultado(content)

    def _extrair_resultado(self, html):
        # abstract method
        raise NotImplementedError("Você deve sobrescrever esse método")

    def __url_consulta(self, concurso):
        return os.path.join(
                    self.URL_BASE, self._url_script + self._url_params).format(
                        **{'loteria': self._loteria, 'concurso': concurso})
