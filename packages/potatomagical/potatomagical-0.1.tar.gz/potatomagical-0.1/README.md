# Magical

A simple magic package.

## Installation

Install via pip: `pip install potatomagical`

## Usage

```python
from potatomagical.magic import do_magic

print(do_magic("Potato"))  # "Potato is now potatomagical!"
```

## Packaging

First, make sure you have the necessary tools installed.

```
pip install twine wheel
```

Then, create a distribution package.


```
python setup.py sdist bdist_wheel
```


## Uploading to PyPI

First, check your package with twine.

```
twine check dist/*
```


If everything is okay, upload your package to PyPI.
```
twine upload dist/*
```

Remember, you'll need to create an account on [PyPI](https://pypi.org/) if you haven't already.

This is a very basic example. Depending on your project, you might need to add more information to `setup.py`, add a `MANIFEST.in` file, etc. Check the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/) for more details.
