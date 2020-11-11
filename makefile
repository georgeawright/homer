.PHONY: clear-logs integration lint migrate migrations unit run runserver tests

clear-logs:
	rm -rf logs/

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

runserver:
	pipenv run python manage.py runserver

tests:
	pipenv run python -m pytest tests/unit
	pipenv run python -m pytest tests/integration
