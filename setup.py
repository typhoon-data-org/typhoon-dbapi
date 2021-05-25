import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines(False)

setuptools.setup(
    name="typhoon_dbapi",
    version="0.0.2",
    author='Typhoon Data',
    author_email='info.typhoon.data@gmail.com',
    description="Hooks and functions related to databases compatible with the Python Database API Specification v2.0.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        'postgres': ['psycopg2'],
        'sqlalchemy': ['sqlalchemy'],
        'snowflake': ['snowflake-connector-python'],
        'bigquery': ['google-cloud-bigquery'],
        'duckdb': ['duckdb'],
        'mssql': ['pymssql'],
    },
)