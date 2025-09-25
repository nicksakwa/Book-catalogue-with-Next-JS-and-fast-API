# Stage 1: Build the backend image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy dependency files and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY backend/app /app/app

# The default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]