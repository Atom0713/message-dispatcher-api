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