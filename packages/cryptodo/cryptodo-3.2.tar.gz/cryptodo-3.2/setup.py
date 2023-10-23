from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '3.2'
DESCRIPTION = 'A Python library for text encryption and decryption'
LONG_DESCRIPTION = 'Cryptodo is a Python library that provides various methods for text encryption and decryption. It includes features like Caesar cipher, substitution cipher, and more. This library is designed to be easy to use and can be integrated into your Python projects for secure data handling.'

# Setting up
setup(
    name="cryptodo",
    version=VERSION,
    author="k.a.ishan oshada",
    author_email="ic31908@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['text encryption', 'text decryption', 'Caesar cipher', 'substitution cipher', 'rail fence cipher'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
