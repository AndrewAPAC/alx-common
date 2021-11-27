from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alx-common',
    version='1.0.0',
    author='Andrew Lister',
    author_email='a.lister.hk@gmail.com',
    description='A common library for home development',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['alx', 'alx/data'],
    package_data = {'alx': ['*.ini']},
    zip_safe=True,
    install_requires=['setuptools-git', 'arrow', 'sqlalchemy', 
        'googlefinance.client'],
    include_package_data=True

)



