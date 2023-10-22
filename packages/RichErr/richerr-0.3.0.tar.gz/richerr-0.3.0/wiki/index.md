# Welcome

[![PyPI version](https://badge.fury.io/py/richerr.svg)](https://badge.fury.io/py/richerr)  [![codecov](https://codecov.io/gh/AdamBrianBright/python-richerr/branch/master/graph/badge.svg?token=DDBNKVLZWH)](https://codecov.io/gh/AdamBrianBright/python-richerr) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAdamBrianBright%2Fpython-richerr.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FAdamBrianBright%2Fpython-richerr?ref=badge_shield)  

## RichErr

RichErr is a tiny module that gives you basic error class, which can be used in JSON, dict, list, and other mutation

```python example.py
from richerr import RichErr

print(RichErr.convert(ValueError('Hello world!')).json(indent=2))
```

```json5
{
  "error": {
    "code": 400,
    "exception": "BadRequest",
    "message": "Hello world!",
    "caused_by": {
      "error": {
        "code": 500,
        "exception": "ValueError",
        "message": "Hello world!",
        "caused_by": null
      }
    }
  }
}
```

## Installation

### Poetry

```shell
poetry add RichErr
```

### PIP

```shell
pip install RichErr
```

## Requirements

- [x] Python 3.12+
- [x] No package dependencies

## Plugins

- [x] Supported Django Validation and ObjectNotFound errors
- [x] Supported DRF Validation errors
- [x] Supported Pydantic Validation errors

### Want to add your own error conversion?

Add direct conversion

```python
from richerr import RichErr, GatewayTimeout


class MyTimeoutError(IOError): ...


RichErr.add_conversion(MyTimeoutError, GatewayTimeout)
```

Or add conversion method

```python
from richerr import RichErr


class MyTimeoutError(IOError): ...


def _convert(err: MyTimeoutError):
    return RichErr.from_error(err, message='Something happened', code=500, name='MyTimeoutError')


RichErr.add_conversion(MyTimeoutError, _convert)
```

!!!
Subclasses will be checked before their parent, if multiple classes in same MRO will be registered.
!!!

 [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAdamBrianBright%2Fpython-richerr.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FAdamBrianBright%2Fpython-richerr?ref=badge_large) 