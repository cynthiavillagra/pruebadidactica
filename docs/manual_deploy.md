# Manual Tecnico: Archivos de Deploy (vercel.json / Dockerfile)

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Infrastructure (Deploy)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este manual cubre los archivos de configuracion de **despliegue**: `vercel.json` para Vercel (serverless) y `Dockerfile` para contenedores Docker.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Infrastructure - Deployment |
| **Requisitos No Funcionales** | RNF (Despliegue) |

---

## 2. vercel.json

### 2.1 Proposito

Configura como Vercel despliega la aplicacion Flask como funcion serverless.

### 2.2 Codigo Fuente

```json
{
  "version": 2,
  "builds": [
    {"src": "api/index.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"src": "/static/(.*)", "dest": "/static/$1"},
    {"src": "/(.*)", "dest": "api/index.py"}
  ],
  "env": {
    "FLASK_ENV": "production",
    "FLASK_DEBUG": "0"
  }
}
```

### 2.3 Explicacion de Campos

| Campo | Valor | Proposito |
|-------|-------|-----------|
| `version` | 2 | Version de configuracion |
| `builds.src` | api/index.py | Entry point |
| `builds.use` | @vercel/python | Runtime Python |
| `routes` | [...] | Mapeo de URLs |
| `env` | {...} | Variables por defecto |

### 2.4 Rutas

| Ruta | Destino | Proposito |
|------|---------|-----------|
| `/api/(.*)` | api/index.py | Todas las APIs |
| `/static/(.*)` | /static/$1 | Archivos estaticos |
| `/(.*)` | api/index.py | Todo lo demas (frontend) |

---

## 3. Dockerfile

### 3.1 Proposito

Define la imagen Docker para despliegue en contenedores (Railway, Fly.io, AWS ECS, etc.).

### 3.2 Codigo Fuente

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
ENV FLASK_ENV=production
ENV PORT=8000
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "api.index:app"]
```

### 3.3 Por Que Multi-Stage

**Stage 1 (builder)**:
- Instala dependencias de compilacion (gcc)
- Crea virtualenv con dependencias
- Imagen temporal, no va a produccion

**Stage 2 (runtime)**:
- Solo copia virtualenv ya listo
- Imagen mas pequena (~150MB vs ~500MB)
- Sin herramientas de desarrollo

---

## 4. Diferencias Local vs Nube

### 4.1 Tabla Comparativa

| Aspecto | Local | Vercel | Docker |
|---------|-------|--------|--------|
| **Comando inicio** | `python api/index.py` | Automatico | `docker run` |
| **Servidor** | Flask dev | Vercel runtime | Gunicorn |
| **Puerto** | 5000 | Dinamico | 8000 |
| **Variables** | .env archivo | Dashboard | --env-file |
| **Debug** | Activado | Desactivado | Desactivado |
| **Hot reload** | Si | No | No |
| **Escalado** | N/A | Automatico | Manual |

### 4.2 Variables de Entorno

**Local (.env)**:
```env
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...
FLASK_ENV=development
```

**Vercel (Dashboard)**:
- Settings > Environment Variables
- Agregar cada variable manualmente

**Docker (--env-file)**:
```powershell
docker run --env-file .env.docker app-didactica
```

---

## 5. Prueba de Fuego

### 5.1 Vercel

```powershell
# Instalar CLI
npm install -g vercel

# Login
vercel login

# Deploy de prueba
vercel

# Deploy produccion
vercel --prod
```

### 5.2 Docker

```powershell
# Construir
docker build -t app-didactica .

# Ejecutar
docker run -p 8000:8000 --env-file .env app-didactica

# Verificar
curl http://localhost:8000/api/health
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Estas Configuraciones

| Decision | Justificacion |
|----------|---------------|
| vercel.json simple | Configuracion minima necesaria |
| Multi-stage Docker | Imagen final pequena |
| Gunicorn | Servidor WSGI de produccion |
| Healthcheck | Monitoreo automatico |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Dockerfile single-stage | Imagen muy grande |
| Flask dev en Docker | No apto para produccion |
| vercel.json con rewrites | Menos intuitivo |
| uWSGI | Mas complejo que Gunicorn |

---

## 7. Troubleshooting

### 7.1 Vercel

| Error | Causa | Solucion |
|-------|-------|----------|
| Build failed | requirements.txt | Verificar formato |
| 500 en /api | Variables faltantes | Agregar en Dashboard |
| Archivos no cargan | Rutas incorrectas | Verificar vercel.json |

### 7.2 Docker

| Error | Causa | Solucion |
|-------|-------|----------|
| Port already in use | Puerto ocupado | Cambiar -p 8001:8000 |
| Health check failing | App no inicia | Revisar logs |
| Permission denied | Permisos | Ejecutar con sudo |

---

> **Manual Tecnico**: Archivos de Deploy  
> **Version**: 1.0.0
