# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)

VERSION ?= $(error VERSION is required, e.g. make $@ VERSION=1.2.3)
TAG_PREFIX ?=

test::
	pytest tests

clean::
	rm -fr dist *egg-info doc build alx_common-*

pip::
	pip install --upgrade alx-common

all:: upload pip

install:: all

dist:: clean
	python -m build

upload:: TAG_PREFIX = local-
upload:: release
	twine upload -r local dist/*

release:: test clean dist
	@echo "Releasing version $(VERSION) with tag $(TAG_PREFIX)v$(VERSION)"
	sed -i 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
	git diff --quiet pyproject.toml || git commit -m "Release $(VERSION)" pyproject.toml
	git tag --force $(TAG_PREFIX)v$(VERSION)
	git push origin main
	git push --force origin $(TAG_PREFIX)v$(VERSION)

pypi:: release
	twine upload -r pypi dist/*

testpypi:: TAG_PREFIX = test-
testpypi:: release
	twine upload -r testpypi dist/*
