import os
from distutils.core import setup

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
    version = "0.0.1",
    author = "Wagner Macedo",
    author_email = "wagnerluis1982@gmail.com",
    description = "Gerador e Verificador de Apostas da Loteria (do Brasil)",
    license = "GPL",
    url = "https://github.com/wagnerluis1982/gval",
    package_dir={'': PACKAGE_DIR},
    packages=find_packages(),
    scripts=["scripts/gval-consultar"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Other/Nonlisted Topic",
    ],
)
