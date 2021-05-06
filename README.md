# Task manager
[![Actions Status](https://github.com/valentin-khomutenko/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/valentin-khomutenko/python-project-lvl4/actions)
<a href="https://codeclimate.com/github/vvkh/python-project-lvl4/maintainability"><img src="https://api.codeclimate.com/v1/badges/9a6942d3460d2428aad6/maintainability" /></a>
<a href="https://codeclimate.com/github/vvkh/python-project-lvl4/test_coverage"><img src="https://api.codeclimate.com/v1/badges/9a6942d3460d2428aad6/test_coverage" /></a>

## Simple web app powered by Django
[Checkout online at Heroku.](https://powerful-shore-49500.herokuapp.com)

## Development guide
Assuming you have Python3 and poetry installed:
```bash
    git clone https://github.com/vvkh/python-project-lvl4 && cd python-project-lvl4
    make install  # install dependencies
    make migrate # run migrations in test db
    make up.dev # start dev server locally
```
Code maintenance:
```bash
make format
make lint
make test 
# or
make self-check
```

Before committing:
```bash
make locales
# add translations to *.po files in task_manager/locale
make compiles-locales
```
Deploy current branch to production:
```bash
make deploy
```

## Configuration
App is configured with following environment variables:

| Env | Setting | Locally | In prod| 
|---|---|---|---|
| `ALLOWED_HOSTS`| What hosts app listen when started. Comma-separated if several hosts. | `localhost,127.0.0.1` | Production hostname, currently [powerful-shore-49500.herokuapp.com](https://powerful-shore-49500.herokuapp.com).
| `DJANGO_SECRET_KEY`| Key used in Django's built-in security features. | Doesn't matter. | Keep in secret.
| `DATABASE_URL` | Connection url for PostgreSQL db. Sqlite3 is used if setting is unset | unset. | Managed automatically by Heroku. 
| `ROLLBAR_ACCESS_TOKEN`| Access token for [rollbar.com](https://rollbar.com) | Doesn't matter. | Keep in secret.
| `DEBUG` | Defines whether full  stacktrace is printed on exceptions or just `500 server error`. | `on` | `off`

Local environment variables are managed by `.env` file, production environment is managed either by `heroku config` command or in heroku dashboard.