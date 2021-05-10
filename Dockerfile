FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y pipenv \
    && rm -rf /var/lib/apt/lists/*

RUN set -ex && mkdir /app

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system

EXPOSE 8000

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port 8000
