import setuptools
from pathlib import Path

setuptools.setup(
    name="abdulpdf2text",  # a unique name, which doesn't conflict with other name in pypi.org
    version="1.0",
    long_description=Path('README.md').read_text(),
    # excluding data and tests folders
    packages=setuptools.find_packages(exclude=['data', 'tests'])
)
