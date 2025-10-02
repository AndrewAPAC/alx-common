# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)

VERSION ?= $(error VERSION is required, e.g. make $@ VERSION=1.2.3)
TAG_PREFIX ?=
TAG_SUFFIX ?=

test::
	pytest tests

clean::
	rm -fr dist *egg-info docs build alx_common-*

pip::
	pip install --upgrade alx-common

# Check for uncommitted changes
check-clean:
	@CHANGED=$$(git diff --name-only); \
	STAGED=$$(git diff --cached --name-only); \
	if [ -n "$$CHANGED" ] || [ -n "$$STAGED" ]; then \
		echo "-------------------------------------------"; \
		echo "Error: you have uncommitted changes!"; \
		if [ -n "$$CHANGED" ]; then \
			echo "Modified/unstaged files:"; \
			echo "$$CHANGED"; \
		fi; \
		if [ -n "$$STAGED" ]; then \
			echo "Staged but uncommitted files:"; \
			echo "$$STAGED"; \
		fi; \
		echo "-------------------------------------------"; \
		exit 1; \
	fi

local:: clean
	python -m build
	twine upload -r local dist/*
	pip install --index-url http://pypi:8083/simple alx-common

dist:: clean check-clean test
	@echo "Building version $(VERSION)"
	sed -i 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
	git diff --quiet pyproject.toml || git commit -m "Release $(VERSION)" pyproject.toml

release:: dist
	@echo "Releasing version $(VERSION) with tag $(TAG)"
	git tag $(TAG)
	git push origin main
	git push origin $(TAG)

pypi:: TAG=v$(VERSION)
pypi:: release

testpypi::
	@SUFFIX=$$(date +%Y%m%d%H%M); \
	TEST_VERSION=$(VERSION).dev$$SUFFIX; \
	TAG=v$$TEST_VERSION; \
	echo "Building test version $$TEST_VERSION"; \
	$(MAKE) VERSION=$$TEST_VERSION TAG=$$TAG release
