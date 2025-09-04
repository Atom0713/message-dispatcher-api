FROM python:3.13.7-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry==2.1.4 \
    && poetry install

COPY /app .

CMD ["fastapi", "run", "src/service/app.py"]
