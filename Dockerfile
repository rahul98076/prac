FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app.py .
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 5000
CMD ["python", "app.py"]