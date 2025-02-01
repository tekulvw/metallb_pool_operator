FROM python:3.13-alpine

ENV PYTHON_UNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.5.26 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src

RUN uv sync --frozen --no-dev

ENV UV_NO_SYNC=1

CMD ["uv", "run", "--", "python", "-m", "metallb_pool_operator"]
