FROM python:3.10-slim-bookworm

WORKDIR /app
COPY . /app

# Run as root for apt install
USER root
RUN apt-get update -y && \
    apt-get install -y awscli && \
    rm -rf /var/lib/apt/lists/*

# Then install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Optional: switch to non-root for security
# USER app

EXPOSE 8080
CMD ["python", "app.py"]
