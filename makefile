.PHONY: clear-logs integration lint unit run log-viewer tests

clear-logs:
	rm -rf logs/
	mkdir logs

integration:
	pipenv run python -m pytest tests/integration

lint:
	pipenv run flake8 .

log-viewer:
	node log_viewer.js

run:
	pipenv run python main.py

tests:
	pipenv run python -m pytest tests/unit
	pipenv run python -m pytest tests/integration

unit:
	pipenv run python -m pytest tests/unit

