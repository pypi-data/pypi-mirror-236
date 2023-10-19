from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.32'
DESCRIPTION = 'A package to scrape SEC data'
LONG_DESCRIPTION = 'A package that allows developers to pull reports from publicly listed companies via the SEC'

# Setting up
setup(
    name="sec_stream",
    version=VERSION,
    author="Noah Taylor",
    author_email="nstaylor03@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    data_files=[('sec_stream', ['sec_stream/tickers.json'])],
    install_requires=[
        'lxml','requests','beautifulsoup4'
    ],
    keywords=['python', 'sec', 'finance', 'requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)