test::
	pytest tests

clean::
	rm -fr dist *egg-info doc build alx_common-*

pip::
	pip install --upgrade alx-common

all:: clean test dist upload pip

install:: all

dist:: clean
	python -m build

upload::
	twine upload -r local dist/*
