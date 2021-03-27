up:
	gunicorn task_manager.server.wsgi

up.dev:
	poetry run python task_manager/manage.py runserver

install:
	poetry install

format:
	poetry run autopep8 -r --in-place task_manager tests

lint:
	poetry run autopep8 -r --diff --exit-code task_manager tests
	poetry run flake8 task_manager tests
	poetry run mypy task_manager tests

test:
	poetry run pytest --cov-report term --cov-report xml --cov=task_manager  tests

migrate:
	poetry run python3 task_manager/manage.py makemigrations
	poetry run python3 task_manager/manage.py migrate

check-locales: locales compiled-locales
	if [[ `git status task_manager/locale --porcelain` ]]; then \
  		echo "locales is not up to date, did you run 'make locales && make compiled-locales'?" \
  		exit 1 \
	fi


locales:
	cd task_manager && poetry run django-admin makemessages -l ru

compiled-locales:
	cd task_manager && poetry run django-admin compilemessages -l ru
