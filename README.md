# setuptools-meta

[![Build Status](https://travis-ci.org/noirbizarre/setuptools-meta.svg?branch=master)](https://travis-ci.org/noirbizarre/setuptools-meta)

Easily store custom metadata with setuptools.

## Install

Adds `setuptools-meta` to your `setup.py` `setup_requires`:

```python
from setuptools import setup

setup(
    ...
    setup_requires=['setuptools-meta'],
    ...
)
```
`setuptools` will automatically install it on first `python setup.py` invocation.

## Usage

Add you custom metadata to the `meta` dict:

```python
#!/usr/bin/env python
from setuptools import setup

setup(
    ...
    setup_requires=['setuptools-meta'],
    meta={
        'meta1': 'value1',
        'meta2': 'value2',
    },
    ...
)
```

Values can be retrieved at runtime with `pkg_resources`:

```python
import json
import pkg_resources

distrib = pkg_resources.get_distribution('my-package')
meta = json.loads(distrib.get_metadata('meta.json'))
assert meta['meta1'] == 'value1'
assert meta['meta2'] == 'value2'
```
