from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1958'

# Setting up
setup(
    name="discordselfutilzzzy",
    version=VERSION,
    author="realfelon",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'discord', 'self', 'discordselfbot', 'discordself', 'sockets', 'automation'],  # Fixed the typo here
    classifiers=[
        "Development Status :: 3 - Alpha",  # Changed "Development Status" to a valid value
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
