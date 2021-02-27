up:
	gunicorn task_manager.wsgi

up.dev:
	poetry run python3 task_manager/manage.py runserver

install:
	poetry install

lint:
	poetry run flake8 task_manager
	poetry run mypy task_manager

migrate:
	poetry run python3 task_manager/manage.py makemigrations
	poetry run python3 task_manager/manage.py migrate