# Multi-stage Dockerfile for LLM Customer Support Agent
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/documents data/faiss_index data/vector_db

# Expose ports
EXPOSE 8000 8501

# Default command (can be overridden)
CMD ["python", "api/main.py"]

