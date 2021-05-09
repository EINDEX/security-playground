FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update \
    && apt install -y pipenv \
    && rm -rf /var/lib/apt/lists/*

RUN set -ex && mkdir /app

WORKDIR /app

ONBUILD COPY Pipfile Pipfile
ONBUILD COPY Pipfile.lock Pipfile.lock

ONBUILD RUN set -ex && pipenv install --deploy --system

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000
