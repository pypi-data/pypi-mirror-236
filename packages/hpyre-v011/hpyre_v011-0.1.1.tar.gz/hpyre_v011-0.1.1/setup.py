from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.1'
DESCRIPTION = 'Electroporation data analysis'
LONG_DESCRIPTION = 'A package that allows to analyze electroporation data(voltage and current).'

# Setting up
setup(
    name="hpyre_v011",
    version=VERSION,
    author="Pedro Paulo",
    author_email="<ppaulo437@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'scipy', 'matplotlib', 'tk', 'lecroyscope', 'isfreader'],
    keywords=['python', 'electroporation', 'fft'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)