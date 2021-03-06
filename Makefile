up:
	gunicorn task_manager.wsgi

up.dev:
	poetry run python manage.py runserver

install:
	poetry install

format:
	poetry run autopep8 -aa -r --in-place task_manager tests

lint:
	poetry run autopep8 -aa -r --diff --exit-code task_manager tests
	poetry run flake8 task_manager tests
	poetry run mypy task_manager tests

test:
	poetry run pytest --cov-report term --cov-report xml --cov=task_manager  tests

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

locales:
	cd task_manager && poetry run django-admin makemessages -l ru

compiled-locales:
	cd task_manager && poetry run django-admin compilemessages -l ru

self-check: format lint test

deploy:
	branch=$$(git branch --show-current) && echo $$branch && read -p "Are you sure that you want to deploy branch $${branch} to production? (y/n)" confirm && [[ $$confirm == [yY] ]] && git push heroku $$branch:main || exit 1
