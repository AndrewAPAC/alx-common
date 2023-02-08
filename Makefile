default::

clean::
	rm -fr dist *egg-info

install:: clean dist upload

dist:: clean
	python setup.py sdist

upload:: install
	twine upload -r local dist/*

