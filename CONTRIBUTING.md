## Code Quality

We use two techniques to maintain Python code quality:

* [flake8](https://pypi.python.org/pypi/flake8), configured by `setup.cfg`
* `scripts/pre-commit` (git hook)

Build the Makefile's _app_ target (part of the default target) to install the pre-commit hook to prevent builds from failing because of PEP8 violations. In addition to using flake8, this hook also executes the sample pre-commit hook.
