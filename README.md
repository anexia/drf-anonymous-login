## DRF Anonymous Login

[![PyPI version](https://img.shields.io/pypi/v/drf-anonymous-login.svg)](https://pypi.org/project/drf-anonymous-login/)
[![Run linter and tests](https://github.com/anexia/drf-anonymous-login/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/drf-anonymous-login/actions/workflows/test.yml)
[![Codecov](https://img.shields.io/codecov/c/gh/anexia/drf-anonymous-login)](https://codecov.io/gh/anexia/drf-anonymous-login)

Django rest framework module to allow login via token (without User instance). Any request with valid token in the
AUTH_HEADER (name configurable via `setting.py`, "HTTP_X_AUTHORIZATION_ANONYMOUS" by default) will be accepted.

### Installation

1. Install using pip:

```shell
pip install drf-anonymous-login
```

2. Integrate `drf_anonymous_login` into your `settings.py`

```python
INSTALLED_APPS = [
    # ...
    'drf_anonymous_login',
    # ...
]
```

### Usage

There are multiple ways to include the `AnonymousLogin` functionality to your endpoints. We recommend to use one of
the following approaches:

1. Inherit from the `AnonymousLoginAuthenticationModelViewSet` for any model that is supposed to be accessible via 
valid token header. You'll find a simple exemplary usage scenario provided the [testapp](tests/testapp/views.py).

OR

2. Directly add the `AnonymousLoginAuthentication` and `IsAuthenticated` to your ViewSet's `authentication_classes` and
   `permission_classes` as implemented in the [AnonymousLoginAuthenticationModelViewSet](drf_anonymous_login/views.py).

## Unit Tests

See folder [tests/](tests/). The provided tests cover these criteria:
* success:
  * access public endpoint without token
  * access private endpoint with valid token
  * cleanup task does not remove tokens before their expiration_datetime
  * cleanup task removes tokens after their expiration_datetime
* failure:
  * access private endpoint without token
  * access private endpoint with invalid token
  * access private endpoint with expired token

Follow below instructions to run the tests.
You may exchange the installed Django and DRF versions according to your requirements. 
:warning: Depending on your local environment settings you might need to explicitly call `python3` instead of `python`.
```bash
# install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# setup environment
pip install -e .

# run tests
cd tests && python manage.py test
```

### Contributing

Contributions are welcomed! Read the [Contributing Guide](CONTRIBUTING.md) for more information.

### Licensing

See [LICENSE](LICENSE) for more information.
