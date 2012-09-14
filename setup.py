import codecs
import os
from setuptools import setup

PACKAGE_DIR = 'src'

def find_packages():
    packages = []

    os.chdir(PACKAGE_DIR)
    for root, dirs, files in os.walk('gval'):
        if '__init__.py' in files:
            packages.append(root.replace(os.sep, '.'))
    os.chdir('..')

    return packages

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
    packages = find_packages(),
    entry_points = {
        "console_scripts": ["gval = gval.script:main"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Other/Nonlisted Topic",
    ],
)
