# Contributing to ALX-Common

🎉 First of all — thank you for considering contributing to ALX-Common!

ALX-Common is a reusable Python framework designed for infrastructure automation, monitoring, reporting, and internal tooling. It aims to simplify repetitive operational tasks and enable maintainable automation systems.

---

## How to Contribute

There are many ways you can help:

- 📦 Submitting bug reports
- 💡 Suggesting new features or improvements
- 🔨 Submitting pull requests (code contributions)
- 📖 Improving documentation

---

## Code Contributions

If you'd like to contribute code:

1. **Fork the repository** on GitHub
2. Create a new branch:
   `git checkout -b feature/my-feature-name`
3. Make your changes
4. Write or update unit tests if applicable
5. Build and run tests locally:
  * `pytest`
6. Build the documentation:
  * `make doc`
7. Submit a pull request describing your change 

## Coding Style
  * Python 3.7+ (Python 3.9+ preferred)
  * Follow PEP 8
  * Use meaningful docstrings — this project uses pdoc for auto-generated documentation
  * Keep code well-organized by module (i.e. alx.app, alx.db_util, alx.itrs, etc.)

## Development Setup

Clone the repo:
```
git clone https://github.com/YOUR_GITHUB_USERNAME/alx-common.git
cd alx-common
```
Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
Install requirements:
```
pip install -r requirements.txt
```
Build the package:
```
make dist
```
Generate documentation:
```
make doc
```
## Reporting Issues

If you encounter a bug or want to request a feature:
  * Please open an issue in GitHub Issues
  * Include as much detail as possible:
  * Environment (Python version, OS, etc.)
  * Steps to reproduce
  * Expected vs. actual behavior
  * Stack trace (if applicable)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (GPL-3.0-or-later).

Thank you for your interest in improving ALX-Common! 🚀
