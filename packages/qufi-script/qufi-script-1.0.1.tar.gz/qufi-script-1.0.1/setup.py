from setuptools import setup
from src.qufi import __version__


setup(
    name="qufi-script",
    author="Natanim Negash",
    author_email="natanimn@yahoo.com",
    description="A python package that converts Oromo language script's witten in latin letters to geez letters",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    url='https://github.com/natanimn/Qufi',
    packages=['qufi'],
    keywords=["fidel", "python", "alphabet", "amharic", "oromo", "letters", "letters convertors",
              "geez letters", "geez", 'qube'],
    version=__version__,
    license="GPLv3"
)