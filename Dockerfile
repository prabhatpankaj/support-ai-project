# -----------------------------------------
# Base image
# -----------------------------------------
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Ensure database directory exists
RUN mkdir -p db

# Default command (can be overridden)
CMD ["python", "new_way.py"]
