from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alx-common',
    version='0.1',
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
    packages=['alx'],
    package_data = {'alx': ['*.ini']},
    zip_safe=True,
    install_requires=['setuptools-git', 'arrow', 'sqlalchemy', 
        'googlefinance.client'],
    include_package_data=True

)



