clean::
	rm -fr dist *egg-info doc build alx_common-*

pip::
	pip install --upgrade alx-common

install:: clean dist upload doc pip

dist:: clean
	python -m build

upload::
	twine upload -r local dist/*

doc::
	-mkdir -p doc
	pdoc -o doc ./alx
