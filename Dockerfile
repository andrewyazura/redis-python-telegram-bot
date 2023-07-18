# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

FROM base AS export-requirements-stage
WORKDIR /tmp

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes


FROM base AS run-app-stage
WORKDIR /code

COPY --from=export-requirements-stage /tmp/requirements.txt ./
RUN pip install --upgrade --no-cache-dir --requirement requirements.txt

CMD ["uvicorn", \
    "--host", "0.0.0.0", \
    "--port", "80", \
    "app.main:app" ]

COPY ./telegram_bot ./app
