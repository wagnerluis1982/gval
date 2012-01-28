from distutils.core import setup

def find_packages():
    return ['gval', 'gval.loteria']

setup(
    name = "GVAL",
    version = "0.0.1",
    author = "Wagner Macedo",
    author_email = "wagnerluis1982@gmail.com",
    description = "Gerador e Verificador de Apostas da Loteria (do Brasil)",
    license = "GPL",
    url = "https://github.com/wagnerluis1982/gval",
    package_dir={'': 'src'},
    packages=find_packages(),
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
