ARG INFRAHUB_BASE_VERSION=1.2.4
FROM registry.opsmill.io/opsmill/infrahub:${INFRAHUB_BASE_VERSION}

# Install specific package
WORKDIR /opt/local
COPY pyproject.toml poetry.lock README.md ./
COPY service_catalog/ service_catalog/

RUN poetry install --no-ansi --no-interaction

WORKDIR /source