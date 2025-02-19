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

install:: clean dist upload doc

dist:: clean
	python setup.py sdist

upload:: install
	twine upload -r local dist/*

doc::
	-mkdir -p doc
	pdoc -o doc $(sources)
