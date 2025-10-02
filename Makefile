# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)

VERSION ?= $(error VERSION is required, e.g. make $@ VERSION=1.2.3)
TAG_PREFIX ?=

test::
	pytest tests

clean::
	rm -fr dist *egg-info docs build alx_common-*

pip::
	pip install --upgrade alx-common

all:: dist upload pip

install:: all

dist:: clean test
	@echo "Building version $(VERSION)"
	sed -i 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
	git diff --quiet pyproject.toml || git commit -m "Release $(VERSION)" pyproject.toml
	python -m build

upload:: dist release
	twine upload -r local dist/*

release:: dist
	@echo "Releasing version $(VERSION) with tag $(TAG_PREFIX)v$(VERSION)"
	git tag --force $(TAG_PREFIX)v$(VERSION)
	git push origin main
	git push --force origin $(TAG_PREFIX)v$(VERSION)

pypi:: release
	twine upload -r pypi dist/*

testpypi:: TAG_PREFIX = test-
testpypi:: release
	twine upload -r testpypi dist/*
