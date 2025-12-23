# ===========================================================================
# Dockerfile - App Didactica CRUD
# ===========================================================================
# Imagen multi-stage para produccion
# Compatible con: Docker, Railway, Fly.io, etc.
# ===========================================================================

# ---------------------------------------------------------------------------
# STAGE 1: Builder
# ---------------------------------------------------------------------------
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias de compilacion
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de capas)
COPY requirements.txt .

# Instalar dependencias en un virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------------------
# STAGE 2: Runtime
# ---------------------------------------------------------------------------
FROM python:3.11-slim as runtime

WORKDIR /app

# Copiar virtualenv del builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar codigo de la aplicacion
COPY . .

# Variables de entorno por defecto
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV PORT=8000

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Comando de inicio
# POR QUE GUNICORN: Servidor WSGI de produccion (Flask dev server no es seguro)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "api.index:app"]
