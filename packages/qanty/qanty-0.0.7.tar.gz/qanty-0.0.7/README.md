[![Release](https://github.com/grupodyd/python-qanty/actions/workflows/python-publish.yml/badge.svg)](https://github.com/grupodyd/python-qanty/actions/workflows/python-publish.yml)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![pypi](https://badge.fury.io/py/qanty.svg)](https://pypi.org/project/qanty/)
[![PyPI](https://img.shields.io/pypi/pyversions/qanty.svg)](https://pypi.python.org/pypi/qanty)
# python-qanty
Python package for integration of Qanty in other applications

### Supported Python Versions

This library supports the following Python implementations:

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

## Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a
package manager for Python.

```shell
pip3 install qanty
```

### Test your installation

Try listing your company branches. Save the following code sample to your computer with a text editor. Be sure to update the `auth_token`, and `company_id` variables.

```python
from qanty import Qanty

# Your Auth Token
client = Qanty(auth_token="your_auth_token", company_id="your_company_id")

branches = client.get_branches()
for branch in branches:
    print(f"Branch ID {branch.id}, name {branch.name}")
```
