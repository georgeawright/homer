.PHONY: clear-logs integration lint migrate migrations unit run runserver runsyncdb setup tests

clear-logs:
	rm -rf logs/
	mkdir logs

integration:
	pipenv run python -m pytest tests/integration

lint:
	pipenv run flake8 .

migrate:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate

migrations:
	pipenv run python manage.py makemigrations

unit:
	pipenv run python -m pytest tests/unit

run:
	pipenv run python main.py

run-test:
	pipenv run python test.py

runserver:
	pipenv run python manage.py runserver

runsyncdb:
	pipenv run python manage.py migrate --run-syncdb

setup:
	export DJANGO_SETTINGS_MODULE=runrecord.settings

tests:
	pipenv run python -m pytest tests/unit
	pipenv run python -m pytest tests/integration
