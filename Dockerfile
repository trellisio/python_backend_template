# syntax=docker/dockerfile:1

#################################################
# Setup Shared Environment
#################################################
FROM python:3.12-slim as base
    # Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NOT_INTERACTION=1 \
    # Paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
# Add to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

#################################################
# Build Dependencies + Create Virtual Environment
#################################################
FROM base as builder
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    # for building dependencies
    build-essential \
    # for installing poetry
    curl
# Install poetry with cache mount
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -
# Copy project requirement files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
# Install runtime dependencies
RUN --mount=type=cache,target=/root/.cache \
    poetry install --without dev,test,docs

#################################################
# Development
#################################################
FROM base as dev
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH
# Copy in poetry + venv
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
# Install dev dependencies
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with dev,test
WORKDIR /app
EXPOSE 8000
CMD ["uvivorn", "--reload", "app:app"]

#################################################
# Production
#################################################
FROM base as prd
ENV FASTAPI_ENV=production
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
WORKDIR /app
COPY ./app /app/
CMD ["uvicorn", "app:app"]