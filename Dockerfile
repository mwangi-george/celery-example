# Start from a slim Python image
FROM python:3.11-slim

# Set workdir inside the container
WORKDIR /app

# Install system deps (optional but good for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Install uv using pip
RUN pip install --no-cache uv

# Copy requirements file separately for caching
COPY requirements.txt .

# Install dependencies with uv (instead of pip)
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command: run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
