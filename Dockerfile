# Use official Python runtime as the base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first (optimizes caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to wait for the database and then run the app
CMD ["sh", "-c", "python wait_for_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]