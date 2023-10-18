# Cookie's Utilities

Utility functions and classes.

<!-- - [TestPyPI](https://test.pypi.org/project/cookies-utilities/) -->
<!-- - [PyPI](https://pypi.org/project/cookies-utilities/) -->
- [Documentation (released)](https://cookies-utilities.readthedocs.io/en/stable/)
- [Documentation (main branch HEAD)](https://cookies-utilities.readthedocs.io/en/latest/)

---

## Installation (for Users)

You can install the release version from PyPI.

```
pip install cookies_utilities
```

If you want to use the latest version that has not been released, clone this repository and install from the local directory.

```
git clone https://github.com/CookieBox26/cookies_utilities.git
cd cookies_utilities
pip install .
```

## Development Guide (for Developers)

Please execute the following at the root of the repository.

### Test locally

Please run the following commands.

```
git clone https://github.com/CookieBox26/cookies_utilities.git
cd cookies_utilities
# make some changes to the code
pip install -e .  # install the package in editable mode
python -m unittest discover tests -v  # test
```
If an error occurs, you can fix the code and rerun the tests without having to reinstall the package.

### Update documentation

If you add a new function or class, please update the documentation accordingly.

```
cd docs
vi source/cookies_utilities.rst  # add a new function or class
./make.bat html  # or 'make html' (not on Windows)
# Please open 'docs/build/html/index.html' in your browser and check the content.
cd ..
```

If you are not an administrator, please open a pull request at this point.

### Build and upload the distribution archives (for administrator only)

Please run the following commands. More details are [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).

```
pip install --upgrade build  # upgrade 'build'
python -m build
```

The following files will be generated.

```
./dist/cookies_utilities-0.0.1.tar.gz
./dist/cookies_utilities-0.0.1-py3-none-any.whl
```

Then please run the following commands. More details are [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives).

```
pip install --upgrade twine
python -m twine upload --repository testpypi dist/*  # TestPyPI
python -m twine upload dist/*  # PyPI
```

