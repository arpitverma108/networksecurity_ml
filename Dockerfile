FROM python:3.10-slim-bookworm

WORKDIR /app

# Install system dependencies first (better layer caching)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends awscli && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code last
COPY . /app

# Create non-root user for security
RUN useradd -m -u 1000 app && \
    chown -R app:app /app

# Switch to non-root user
USER app

EXPOSE 8080
CMD ["python", "app.py"]