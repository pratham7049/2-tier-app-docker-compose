# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "app.py"]
