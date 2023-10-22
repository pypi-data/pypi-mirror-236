from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.0.2'

# Setting up
setup(
    name="ayatotest1",
    version=VERSION,
    author="realfelon",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'discord', 'self', 'discordselfbot', 'discordself', 'sockets', 'automation'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
