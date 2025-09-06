APP_NAME = message-dispatcher-api

build:
	docker build -t $(APP_NAME):dev .

cli:
	docker run -it --rm $(APP_NAME):dev bash

build_venv:
	pip install poetry=="2.1.4"
	poetry install

run:
	docker run --rm -p 8000:8000 $(APP_NAME):dev

pytest:
	docker run --rm $(APP_NAME):dev sh -c pytest .

ruff-format:
	docker run --rm $(APP_NAME):dev sh -c "ruff format"

isort: 
	docker run --rm $(APP_NAME):dev sh -c "ruff check --select I --fix"

ruff-check:
	docker run --rm $(APP_NAME):dev sh -c "ruff check ."

ruff:
	docker run --rm $(APP_NAME):dev sh -c "ruff check --fix ."

fix: ruff ruff-format
format: ruff-format
check: ruff-check

test: ruff-check pytest