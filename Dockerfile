# ─── Stage 1: Build dependencies ─────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only Python dependencies (no gcc/libpq-dev needed for psycopg2-binary)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── Stage 2: Final image ────────────────────────────────────────────────────
FROM python:3.12-slim

# Declare environment variables
ENV PORT=8080 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create and switch to non-root user
RUN addgroup --system appgroup \
 && adduser  --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app
USER appuser

# Expose the application port
EXPOSE ${PORT}

# Start the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
