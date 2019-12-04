default::

clean::
	rm -fr dist *egg-info

install:: dist upload

dist::
	python setup.py sdist

upload::
	twine upload -r local dist/*

