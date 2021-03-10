up:
	gunicorn task_manager.wsgi

up.dev:
	poetry run python3 task_manager/manage.py runserver

install:
	poetry install

lint:
	poetry run flake8 task_manager
	poetry run mypy task_manager

test:
	poetry run pytest --cov-report term --cov-report xml --cov=task_manager  tests

migrate:
	poetry run python3 task_manager/manage.py makemigrations
	poetry run python3 task_manager/manage.py migrate

locales:
	cd task_manager && poetry run django-admin makemessages -l ru

compiled-locales:
	cd task_manager && poetry run django-admin compiemessages -l ru
