FastAPI Example Todo Application
====================

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://github.com/tiangolo/fastapi)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat)](https://github.com/pre-commit/pre-commit)

FastAPI example ToDo Application with user authentication.

### Stack:
- FastAPI
- SQLAlchemy
- Alembic

Developing
-----------

Install pre-commit hooks to ensure code quality checks and style checks


    $ make install_hooks

Then see `Configuration` section

You can also use these commands during dev process:

- to run mypy checks


      $ make types

Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
SECRET_KEY=changeme
DATABASE_URL=sqlite:///todo.db
```

Local install
-------------

Setup and activate a python3 virtualenv via your preferred method. e.g. and install production requirements:


    $ make ve

For remove virtualenv:


    $ make clean


Local run
-------------
Make migration to create tables

    $ make migration message="Create tables"
    $ make migrate

Run server with settings:

    $ make runserver

Register user:

    $ curl -X 'POST' \
        'http://0.0.0.0:5000/api/v1/user' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "test-user",
            "email": "test@test.com",
            "full_name": "Test Test",
            "password": "weekpassword"
        }'

If everything is fine, check this endpoint:

    $ curl -X "GET" http://0.0.0.0:5000/api/v1/status

Expected result:

```
{
  "success": true,
  "version": "<version>",
  "message": "FastAPI Todo Application"
}
```
