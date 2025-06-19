FROM python:3.11-slim as base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base as test
COPY . .
ENV FLASK_ENV=testing
ENV PYTHONPATH=/app
CMD ["pytest", "--cov=app", "--cov-report=xml"]

FROM base as production
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]