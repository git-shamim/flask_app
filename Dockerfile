# ─── Stage 1: Build dependencies ─────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory to FlaskApp (your actual Flask app root)
WORKDIR /app/FlaskApp

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY FlaskApp/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── Stage 2: Final image ────────────────────────────────────────────────────
FROM python:3.12-slim

ENV PORT=8080 \
    PYTHONUNBUFFERED=1

# Set working directory again to match app structure
WORKDIR /app/FlaskApp

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy Flask app source code
COPY FlaskApp/ .

# Create non-root user
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app
USER appuser

# Expose Cloud Run's expected port
EXPOSE ${PORT}

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
