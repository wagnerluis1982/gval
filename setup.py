import codecs
import os
from setuptools import setup, find_packages

# Removendo checagem do README
from setuptools.command.sdist import sdist
sdist.check_readme = lambda self: None

PACKAGE_DIR = 'src'

setup(
    name = "GVAL",
    version = "0.0.6",
    author = "Wagner Macedo",
    author_email = "wagnerluis1982@gmail.com",
    description = "Gerador e Verificador de Apostas da Loteria (do Brasil)",
    long_description = codecs.open("README.md", 'r', encoding='utf-8').read(),
    license = "GPL",
    url = "https://github.com/wagnerluis1982/gval",
    package_dir = {'': PACKAGE_DIR},
    packages = find_packages(PACKAGE_DIR),
    install_requires = ["PyYAML"],
    entry_points = {
        "console_scripts": ["gval = gval.script:main"],
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Other/Nonlisted Topic",
    ],
)
