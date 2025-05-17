from setuptools import setup
from alx import __author__, __version__, __author_email__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alx-common',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description='A common library for home development',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL v3",
    packages=['alx', 'alx/itrs'],
    package_data = {'alx': ['*.ini']},
    zip_safe=True,
    install_requires=['setuptools-git', 'arrow', 'sqlalchemy',
                      'cryptography'],
    include_package_data=True
)
