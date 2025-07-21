# ─── Base Image ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─── Environment Variables ──────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HF_HOME=/app/hf_models

# ─── Set Work Directory ─────────────────────────────────────────────────────
WORKDIR /app

# ─── System-Level Dependencies ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    libgl1-mesa-glx \
    curl \
 && rm -rf /var/lib/apt/lists/*

# ─── Install Python Dependencies Early for Layer Caching ────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ─── Download SpaCy Model + Preload HF Model Before Code Copy ──────────────
# This allows caching even if app code changes
RUN python -m spacy download en_core_web_sm

# ─── Copy Application Code ──────────────────────────────────────────────────
COPY . .

# ─── Preload Hugging Face Model ─────────────────────────────────────────────
#RUN mkdir -p $HF_HOME \
# && python preload_model.py

# ─── Create Non-Root User ───────────────────────────────────────────────────
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser \
 && chown -R appuser:appgroup /app
USER appuser

# ─── Expose and Start ───────────────────────────────────────────────────────
EXPOSE ${PORT}
CMD ["gunicorn", "--workers", "2", "--threads", "4", "--timeout", "180", "--bind", "0.0.0.0:8080", "index:app"]
