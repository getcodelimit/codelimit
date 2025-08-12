FROM python:3.12-slim-bookworm

RUN pip install "uv==0.8.3"

RUN mkdir /app
COPY pyproject.toml uv.lock README.md /app
COPY codelimit /app/codelimit
WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --locked --dev

ENTRYPOINT ["/usr/local/bin/codelimit"]
