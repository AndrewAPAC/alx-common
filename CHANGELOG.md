# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- The first public release was 2.7.5 on August 25, 2025

## [2.8.9] - Unreleased

### Added

### Changed

- There were a `Dataview` spanned column heading in the html generated
by `alx.itrs.alert.py`. It was unnecessary. Moved the `Value` row to right
under the `Severity` row so a small change visually.

### Fixed

## [2.8.8] - 2026-01-01

### Added

- New html routines: `add_code(), add_pre()` and `add_blockquote()`

### Changed

### Fixed

## [2.8.7] - 2025-11-13

### Added

### Changed

### Fixed

- `db_util.run` only returned values for a select statement - added `with` and
statements with `returning`.  Other statements returning values will need
to be handled independently as they are mostly command line functions.

## [2.8.6] - 2025-11-07

Released from dev branch.  Fix in place to prevent again. 2.8.5 was yanked.

## [2.8.5] - 2025-11-07

### Added
- Added `parse_config_section` to parse a section of the config file
without including the `[DEFAULT]` keys
- More tests for `parse_config_section`

### Changed
- Show sql params in `db_utils.run` if passed

### Fixed
- README.md link to CHANGELOG.md
- Tidied up and corrected some documentation
- A type mismatch in `parse_config_section` resulted in an exception
when calling `config.getboolean()`

## [2.8.4] - 2025-10-03

### Added
- GitHub Actions to build and publish wheel and tar.gz for 
https://test.pypi.org/project/alx-common/ and 
https://pypi.org/project/alx-common/
- New Makefile targets for `testpypi` and `pypi`
- Check for checked out files when building pypi target

### Changed
- Changed library logging to level `DEBUG`
- Use trusted publishing instead of API tokens
- Moved `alx.app._create_configuration_files()` to `alx.app.Paths`
to further remove need for ALXapp instantiation in 
`alx.html.ALXhtml()`
- Renamed `_create_configuration_files` to `create_configuration_files`

### Fixed

- `test_alert.py` failure due to config files not existing

## [2.8.3] - 2025-10-02

### Added

- Added CHANGELOG.md and updated supporting documentation / links

### Fixed

- Makefile dependency issues

## [2.8.2] - 2025-10-02

### Added
- GitHub Actions workflow to automatically build and deploy pdoc 
  documentation to GitHub Pages: https://andrewapac.github.io/alx-common
- README.md displayed as landing page in generated docs.
- `alx.__init__.py` sets `__doc__` based on PDOC environment variable.

### Changed
- Cleaned `gh-pages` branch to remove unnecessary files.
- Improved inline docstrings for submodules.

### Fixed
- Fixed missing dependencies in documentation build step.

## [2.8.1] - 2025-08-27

### Changed

- Mostly documentation and cosmetic fixes

## [2.8.0] - 2025-08-27

### Added
- Automatic creation of configuration files in `.config/alx`
including the `key` file.
- Store more paths in the `alx.app.Path` class
- More documentation
- Better release mechanism in GitHub Actions. Later moved to
`Makefile`

### Changed

- Only minimal local `.config/alx/alx.ini` required. Defaults 
are overridden from installed `alx.ini`

### Fixed

- Changed `ALXapp.read_lib_config()` to not require an entire `ALXapp`
class to be instantiated if it has not been already

## [2.7.6] - 2025-08-25

- Initial public release


