# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies without using hashes
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p logs artifacts data/uploads data/processed

# Copy the project files
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Expose Streamlit port
EXPOSE 8501

# Set Streamlit specific environment variables
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Command to run the Streamlit app
CMD ["streamlit", "run", "scripts/app.py"] 