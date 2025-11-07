# Building and Releasing alx-common

This document describes how to build, test, and release the `alx-common` package.

## Prerequisites

- Python 3.x with pip
- pytest for running tests
- build tools: `python -m pip install build twine`
- Git for version control
- Access to PyPI (for public releases) or local PyPI server

## Development Workflow

### Running Tests
```bash
make test
```

This runs the pytest suite in the `tests/` directory.

### Installing Locally

To install the current development version:
```bash
make pip
```

This upgrades your local installation to the latest from PyPI.

### Cleaning Build Artifacts
```bash
make clean
```

Removes `dist/`, egg-info, docs, build directories, and package archives.

## Building for Local PyPI Server

To build and upload to a local PyPI server (http://pypi:8083):
```bash
make local
```

This will:
1. Clean previous builds
2. Build the package using `python -m build`
3. Upload to the local PyPI server
4. Install from the local server

## Release Process

### Releasing to PyPI

**Important:** Ensure all changes are committed before releasing.
```bash
make pypi VERSION=1.2.3
```

This will:
1. Check for uncommitted changes (fails if found)
2. Run tests
3. Update `pyproject.toml` with the new version
4. Commit the version change
5. Create a git tag `v1.2.3`
6. Push to `origin/main`
7. Push the tag

### Test Release (TestPyPI)

To create a test release with a timestamp suffix:
```bash
make testpypi VERSION=1.2.3
```

This creates a version like `1.2.3.dev202501071430` and tags it accordingly.

## Version Management

Versions follow semantic versioning (MAJOR.MINOR.PATCH). The VERSION parameter is required for release targets.

### Custom Tags

You can customize the git tag format:
```bash
make pypi VERSION=1.2.3 TAG_PREFIX=release- TAG_SUFFIX=-stable
```

This would create a tag like `release-v1.2.3-stable`.

## Troubleshooting

### Uncommitted Changes Error

If you see "Error: you have uncommitted changes!" during release:
- Review changes with `git status`
- Commit or stash your changes
- Run the release command again

### Build Failures

If the build fails:
- Ensure all dependencies are installed
- Check that tests pass with `make test`
- Verify `pyproject.toml` syntax is correct

## Manual Build Steps

If you need to build manually:
```bash
# Clean
rm -fr dist *egg-info docs build alx_common-*

# Build
python -m build

# Upload to PyPI
twine upload dist/*

# Or upload to TestPyPI
twine upload -r testpypi dist/*
```