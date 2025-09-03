# Use official Python runtime
FROM python:3.11-slim

# Install system dependencies including git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the main service
CMD ["python", "orchestrator.py"]
