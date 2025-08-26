VERSION ?= $(error VERSION is required, e.g. make $@ VERSION=1.2.3)

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

release::
	@echo "Releasing version $(VERSION)"
	sed -i 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
	git add pyproject.toml
	git commit -m "Release $(VERSION)"
	git tag v$(VERSION)
	git push origin main
	git push origin v$(VERSION)

pypi:: release
	twine upload -r pypi dist/*

testpypi:: release
	twine upload -r testpypi dist/*
