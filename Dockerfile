# ─── Stage 1: Build dependencies ─────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system-level dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── Stage 2: Final image ────────────────────────────────────────────────────
FROM python:3.12-slim

ENV PORT=8080 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies (only lightweight libs for runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create and use non-root user
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app
USER appuser

# Expose port
EXPOSE ${PORT}

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
