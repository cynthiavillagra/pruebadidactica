# App Didactica CRUD de Alumnos

> Sistema CRUD educativo para gestion de alumnos, desarrollado con Clean Architecture y patrones de diseno.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-orange.svg)](https://supabase.com)
[![Tests](https://img.shields.io/badge/Tests-55%20passed-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## Descripcion

Aplicacion web CRUD (Create, Read, Update, Delete) para gestionar datos de alumnos. Desarrollada con propositos **pedagogicos** para ensenar:

- Clean Architecture (Domain, Application, Infrastructure, API)
- Patrones de diseno (Repository, Factory, Singleton, Decorator)
- Backend con Python/Flask
- Frontend moderno con JavaScript vanilla
- Integracion con Supabase (PostgreSQL + Auth)
- Testing automatizado con pytest
- Despliegue multiplataforma (Local, Vercel, Docker)

---

## AI Stack

### Herramientas de IA Utilizadas

| Herramienta | Uso |
|-------------|-----|
| **Google Gemini CLI / Antigravity** | Entorno de desarrollo asistido |
| **Anthropic Claude** | Generacion de codigo y documentacion |

### Advertencias Importantes

> **NO APTO PARA PRODUCCION**

Este proyecto:
- Es un **MVP educativo**, no una aplicacion lista para produccion
- Puede contener **vulnerabilidades de seguridad** no auditadas
- Esta destinado exclusivamente a:
  - Aprendizaje y ensenanza
  - Desarrollo local
  - Prototipos y demos

---

## Estructura del Proyecto

```
app-prueba-didactica/
|-- api/                    # Capa de presentacion (Flask)
|   |-- index.py            # Entry point
|   |-- routes.py           # Endpoints REST
|   |-- middleware/auth.py  # Autenticacion JWT
|
|-- application/            # Capa de aplicacion
|   |-- alumno_service.py   # Casos de uso CRUD
|
|-- domain/                 # Capa de dominio
|   |-- entities/alumno.py  # Entidad con validaciones
|   |-- repositories/       # Interfaces abstractas
|   |-- exceptions.py       # Excepciones de negocio
|
|-- infrastructure/         # Capa de infraestructura
|   |-- config.py           # Variables de entorno
|   |-- supabase_client.py  # Cliente Singleton
|   |-- supabase_alumno_repository.py
|
|-- static/                 # Frontend
|   |-- index.html          # HTML principal
|   |-- css/styles.css      # Estilos (modo oscuro)
|   |-- js/app.js           # Logica + Watchdog
|
|-- tests/                  # Tests automaticos
|   |-- test_alumno.py
|   |-- test_alumno_service.py
|   |-- test_routes.py
|
|-- docs/                   # Documentacion
|-- database/init.sql       # Script de BD
```

---

## Instalacion Rapida

### 1. Clonar y Configurar

```bash
git clone https://github.com/cynthiavillagra/pruebadidactica.git
cd pruebadidactica

python -m venv venv
.\venv\Scripts\Activate  # Windows
pip install -r requirements.txt
```

### 2. Configurar Credenciales

```bash
copy .env.example .env
# Editar .env con credenciales de Supabase
```

### 3. Iniciar Servidor

```bash
python api/index.py
# Abrir http://localhost:5000
```

---

## Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# Resultado esperado: 55 passed
```

---

## API Endpoints

| Metodo | Endpoint | Descripcion | Auth |
|--------|----------|-------------|------|
| GET | `/api/health` | Health check | No |
| GET | `/api/config` | Config publica | No |
| GET | `/api/alumnos` | Listar | Si |
| POST | `/api/alumnos` | Crear | Si |
| GET | `/api/alumnos/{id}` | Obtener | Si |
| PUT | `/api/alumnos/{id}` | Actualizar | Si |
| DELETE | `/api/alumnos/{id}` | Eliminar | Si |

---

## Documentacion

| Documento | Descripcion |
|-----------|-------------|
| [01_planificacion_analisis](docs/01_planificacion_analisis.md) | Requisitos y User Stories |
| [02_a_arquitectura_patrones](docs/02_a_arquitectura_patrones.md) | Clean Architecture |
| [02_b_modelado_datos](docs/02_b_modelado_datos.md) | DER y Diagrama de Clases |
| [03_c_api_dinamica](docs/03_c_api_dinamica.md) | Especificacion API |
| [035_manual_bbdd](docs/035_manual_bbdd.md) | Configuracion Supabase |
| [setup_externo](docs/setup_externo.md) | Guia de APIs externas |
| [plan_uat](docs/plan_uat.md) | Plan de pruebas UAT |
| [manual_testing](docs/manual_testing.md) | Guia de testing |
| [07_despliegue_cierre](docs/07_despliegue_cierre.md) | Deploy y cierre |

---

## Despliegue

### Vercel (Serverless)

```bash
npm i -g vercel
vercel login
vercel --prod
```

### Docker

```bash
docker build -t app-didactica .
docker run -p 8000:8000 --env-file .env app-didactica
```

---

## Seguridad Implementada

| Feature | Implementacion |
|---------|----------------|
| Autenticacion | Supabase Auth + JWT |
| Autorizacion | RLS en PostgreSQL |
| Sesion | Watchdog 15 min inactividad |
| API | Token Bearer requerido |
| Frontend | Credenciales desde /api/config |

---

## Metricas del Proyecto

| Metrica | Valor |
|---------|-------|
| Archivos de codigo | ~15 |
| Lineas de codigo | ~3000 |
| Tests automaticos | 55 |
| Documentos | 12 |
| Cobertura de requisitos | 100% |

---

## Licencia

Este proyecto esta bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Puedes copiar, modificar y distribuir libremente con atribucion.

Ver [LICENSE](LICENSE) para mas detalles.

---

## Autor

Desarrollado con fines educativos utilizando metodologias de desarrollo asistido por IA.

---

> **Version**: 1.0.0  
> **Estado**: COMPLETADO  
> **Fecha**: 2025-12-22
