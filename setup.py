import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines(False)

setuptools.setup(
    name="dbapi_hooks",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
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
    },
)