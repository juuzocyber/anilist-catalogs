# ── Build stage: install dependencies ────────────────────────────────────────
FROM python:3.12-slim AS deps

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt


# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from deps stage (avoids pip in the final image)
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application source
COPY anilist.py cache.py config.py configure.py crypto.py \
     main.py manifest.py models.py settings.py ./

# Hand ownership to appuser
RUN chown -R appuser:appuser /app

USER appuser

# Document the default port (actual value comes from the PORT env var)
EXPOSE ${PORT:-7000}

# Read HOST and PORT from env; fall back to the same defaults as settings.py
ENV HOST=0.0.0.0
ENV PORT=7000

CMD uvicorn main:app --host "${HOST}" --port "${PORT}"
