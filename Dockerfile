FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PIPENV_IGNORE_VIRTUALENVS=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    make \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system

FROM python:3.13-slim AS final

WORKDIR /app

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

COPY --from=builder /usr/local /usr/local

COPY . .

CMD ["make", "start"]
