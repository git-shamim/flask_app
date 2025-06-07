# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Cloud Run
EXPOSE 8080

# Run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

