clean::
	rm -fr dist *egg-info doc build alx_common-*

pip::
	pip install --upgrade alx-common

test::
	pytest tests

install:: clean dist test upload doc pip

dist:: clean
	python -m build

upload::
	twine upload -r local dist/*

doc::
	-mkdir -p doc
	pdoc -o doc ./alx
