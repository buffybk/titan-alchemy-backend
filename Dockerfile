FROM python:3.11-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test
# Copy test files first to avoid caching issues
COPY tests/ ./tests/
COPY app/ ./app/
COPY pytest.ini .
COPY config.py .
COPY run.py .
ENV FLASK_ENV=testing
ENV PYTHONPATH=/app
CMD ["pytest", "--cov=app", "--cov-report=xml"]

FROM base AS production
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]