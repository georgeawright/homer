.PHONY: integration lint unit run

integration:
	pipenv run python -m pytest tests/integration

lint:
	pipenv run flake8 .

unit:
	pipenv run python -m pytest tests/unit

run:
	pipenv run python main.py
