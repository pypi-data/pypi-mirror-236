# django-static-base [![PyPi license](https://img.shields.io/pypi/l/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)

[![PyPi status](https://img.shields.io/pypi/status/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi version](https://img.shields.io/pypi/v/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-static-base.svg)](https://pypi.python.org/pypi/django-static-base)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-static-base.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-static-base.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-static-base/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-static-base?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-static-base/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-static-base/main) [![gitthub.com](https://github.com/DLRSP/django-static-base/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-static-base/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-static-base)

## Requirements
-   Python 3.8+ supported.
-   Django 3.2+ supported.

## Setup
1. Install from **pip**:
    ```shell
    pip install django-static-base
    ```
2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        # ...
        "static_base",
        # ...
    ]
    ```
3. Finally, modify your project `urls.py` with handlers for all errors:
    ```python
    # ...other imports...

    urlpatterns = [
        # ...other urls...
    ]
    ```
4. Execute Django's command `migrate` inside your project's root:
    ```shell
    python manage.py migrate
    Running migrations:
      Applying static_base.0001_initial... OK
    ```

## Run Example Project

```shell
git clone --depth=50 --branch=django-static-base https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
