# pytest-pokie

[![pypi](https://img.shields.io/pypi/v/pytest-pokie.svg)](https://pypi.org/project/pytest-pokie/)
[![license](https://img.shields.io/pypi/l/pytest-pokie.svg)](https://git.oddbit.org/OddBit/pytest-pokie/src/branch/master/LICENSE)

Pytest plugin to run tests on pokie applications

The pytest-pokie plugin extracts the pokie-based Flask application from the global namespace, and exposes a set
of predefined fixtures for pokie structures.

Note: Currently, only PostgreSQL is supported; the configured database user must have database creation/drop privileges;
The plugin also assumes the user can connect to the database 'postgres', as it is used as the default db for
administrative
operations.

## configuration parameters

| Parameter            | Description                                                         |
|----------------------|---------------------------------------------------------------------|
| TEST_DB_NAME         | PostgreSQL test database name                                       |
| TEST_DB_HOST         | PostgreSQL host                                                     |
| TEST_DB_PORT         | PostgreSQL port                                                     |
| TEST_DB_USER         | PostgreSQL user                                                     |
| TEST_DB_PASSWORD     | PostgreSQL password                                                 |
| TEST_DB_SSL          | if True, enforces SSL                                               |
| TEST_MANAGE_DB       | if False, no db is managed via pytest-pokie                         |
| TEST_SHARE_CTX       | if False, create a new application instance between tests (default) |
| TEST_DB_REUSE        | if False, drops and recreates the database between tests (default)  |
| TEST_SKIP_MIGRATIONS | if False, runs migrations when creating the database                |
| TEST_SKIP_FIXTURES   | if False, runs fixtures when creating the database                  |



## application lifecycle

#### TEST_SHARE_CTX

**False (default)**: Each test is run with a separate application instance; the application is bootstrapped at each
test, by using
the existing application factory.

**True**: All tests are run with the same pokie FlaskApplication and Flask instance; services, events, etc. will be
managed
and cached as in a production run.

## database management options

Please note: The credentials provided to the test database **must** have enough privileges for the required operations,
such as creating and dropping databases.

#### TEST_MANAGE_DB

**False (default)**: If TEST_MANAGE_DB is False, database management is completely ignored, and available db connection
is the regular
application connection. All database test configurations are ignored. With this mode, it is up to the developer to
ensure a clean state between database runs.

**True**: If TEST_MANAGE_DB is True, pytest-pokie will manage the database connection using the available test
credentials.
The global database connection is replaced with the test connection, and fixtures and migrations may be executed between
tests.

#### TEST_DB_REUSE

**False (default)**: if TEST_DB_REUSE is False, pytest-pokie will attempt to drop and recreate the test database between
each test.

**True**: if TEST_DB_REUSE is True, pytest-pokie will not drop the testing database if exists. If it doesn't exist, it
will attempt to create the database and optionally run migrations and fixtures, depending on TEST_SKIP_MIGRATIONS and
TEST_SKIP_FIXTURES values.

#### TEST_SKIP_MIGRATIONS

**False (default)**: Existing SQL migrations will be run when the database is recreated.

**True**: Existing SQL migrations are ingored, even if the database is recreated.

#### TEST_SKIP_FIXTURES

**False (default)**:Existing fixtures will be run when the database is recreated.

**True**: Existing fixtures are ingored, even if the database is recreated.

## avaliable fixtures

Note: fixtures depend on the predefined values for the different DI constants as specified on the *pokie.constants*
file.

| Fixture      | Description           |
|--------------|-----------------------|
| pokie_app    | Pokie Flask object    |
| pokie_config | Pokie Config object   |
| pokie_di     | Pokie Di object       |
| pokie_db     | Pokie Database client |
| pokie_client | Flask test client     | 

## writing tests for pokie applications

Pytest must be invoked using the internal pokie pytest runner. The pytest runner will automatically add the pytest-pokie
plugin to pytest. All additional pytest command-line arguments can be specified:

```shell
$ python main.py pytest --help

[Pokie] Running pytest with: ['--help']
usage: main.py [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         only run tests which match the given substring expression. An expression is a python evaluatable expression where all names are substring-matched against test names and their parent classes. Example: -k
                        'test_method or test_other' matches all test functions and classes whose name contains 'test_method' or 'test_other', while -k 'not test_method' matches those that don't contain 'test_method' in their names. -k
                        'not test_method and not test_other' will eliminate the matches. Additionally keywords are matched to classes and functions containing extra names in their 'extra_keyword_matches' set, as well as functions which
                        have names assigned directly to them. The matching is case-insensitive.
  -m MARKEXPR           only run tests matching given mark expression.
                        For example: -m 'mark1 and not mark2'.
  --markers             show markers (builtin, plugin and per-project ones).
  -x, --exitfirst       exit instantly on first error or failed test.
  --fixtures, --funcargs
(...)
$
```

The scaffold structure is similar to the common pytest usage:

```shell
some_module/
  (...)
main.py
tests/
  __init__.py
  some_module/
    __init__.py
    test_something.py  
```

test_something.py:

```python

def test_example_1(pokie_app, pokie_di):
    assert pokie_app is not None
    assert pokie_app.di == pokie_di


def test_example_2(pokie_db, pokie_service_manager):
    assert pokie_db is not None
    assert pokie_service_manager is not None
```

And to run the tests:

```shell
$ python3 main.py pytest
```

## using tox

Example tox.ini:

```ini
[base]
name = module_name

[tox]
envlist =
    py39
    py310

[testenv]
deps = -rrequirements-dev.txt
commands = python3 main.py pytest
```

Example requirements-dev.txt:

```shell
pytest==7.3.1
pytest-cov==4.0.0
pytest-testdox==3.0.1
pokie==0.4.0
pytest-pokie==0.2.0
flake8==6.0.0
flake8_black==0.3.6
coverage==7.2.5
tox==4.5.1
setuptools~=60.0.0
```

Running with tox:

```shell
$ tox -e py310
```
