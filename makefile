.PHONY: lint unit

lint:
	pipenv run flake8 .

unit:
	pipenv run python -m pytest tests/unit
