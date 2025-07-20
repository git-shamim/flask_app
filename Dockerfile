# ─── Base Image ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─── Environment Variables ──────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# ─── Set Work Directory ─────────────────────────────────────────────────────
WORKDIR /app

# ─── System-Level Dependencies ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# ─── Copy Files ─────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

# ─── Create Non-Root User ───────────────────────────────────────────────────
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app
USER appuser

# ─── Expose and Start ───────────────────────────────────────────────────────
EXPOSE ${PORT}
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "index:app"]
