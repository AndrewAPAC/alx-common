default::

sources = \
	alx/app.py \
	alx/date_util.py \
	alx/db_util.py \
	alx/html.py \
	alx/mail.py \
	alx/itrs

clean::
	rm -fr dist *egg-info doc build

pip::
	pip install --upgrade alx-common

install:: clean dist upload doc pip

dist:: clean
	python setup.py sdist

upload::
	twine upload -r local dist/*

doc::
	-mkdir -p doc
	pdoc -o doc $(sources)
