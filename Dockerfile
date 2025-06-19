FROM python:3.11-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test
# Add build argument to force fresh builds
ARG CACHEBUST=1
ARG TIMESTAMP=1
# Copy files to correct locations to avoid double app folder
COPY . .
# Force rebuild by touching files and clear Python cache
RUN find . -name "*.py" -exec touch {} \; && \
    find . -name "*.pyc" -delete 2>/dev/null || true && \
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
ENV FLASK_ENV=testing
ENV PYTHONPATH=/app
CMD ["pytest", "--cov=app", "--cov-report=xml"]

FROM base AS production
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]