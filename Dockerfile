# Use Python 3.11 slim image
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Update system packages and install required dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=80

# Expose the port
EXPOSE 80

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:80/health || exit 1

# Run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:80", "run:app"]