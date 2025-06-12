FROM python:3.12-slim

RUN apt-get update && apt-get install -y libmagickwand-dev

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv sync --locked --no-install-project --no-dev

RUN useradd -m -r appuser && chown -R appuser /app

USER appuser

EXPOSE 8000

COPY --chown=appuser:appuser . .
RUN chmod +x /app/entrypoint.prod.sh

CMD ["/app/entrypoint.prod.sh"]

