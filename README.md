# Typhoon DbAPI Extension

Hooks and functions related to databases compatible with the [Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/).

## Installation

Run `pip install typhoon-dbapi` for the base package including functions and an EchoDb hook for testing purposes as well as SQLite.

## Install extras

For additional databases run:

- **Snowflake**: `pip install typhoon-dbapi[snowflake]`
- **Big Query**: `pip install typhoon-dbapi[bigquery]`
- **Postgres**: `pip install typhoon-dbapi[postgres]`
- **DuckDB**: `pip install typhoon-dbapi[duckdb]`
- **MySQL**: `pip install typhoon-dbapi[mysql]`

## Virtualenv for development

```shell script
python3 -m venv venv_typhoon
source venv_typhoon/bin/activate
python -m pip install -r requirements   # Re-run this every time you add new requirements
```

## Upload to Pypi

Make an account at https://pypi.org/account/register/.
Edit the setup.py to include project name, desired version, description etc. https://docs.python.org/3/distutils/setupscript.html
Run `make typhoon-extension` and use the user and password you created to upload.

## Upload docs to github pages

**Coming soon...**
