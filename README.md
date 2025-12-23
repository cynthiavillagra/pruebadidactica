# App Didactica CRUD de Alumnos

> Sistema CRUD educativo para gestion de alumnos, desarrollado con arquitectura Clean Architecture.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-orange.svg)](https://supabase.com)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

---

## Descripcion

Aplicacion web CRUD (Create, Read, Update, Delete) para gestionar datos de alumnos. Desarrollada con propositos **pedagogicos** para ensenar:

- Arquitectura Clean Architecture
- Patrones de diseno (Repository, Factory, Singleton, etc.)
- Desarrollo backend con Python/Flask
- Integracion con Supabase (PostgreSQL + Auth)
- Despliegue multiplataforma (Local, Vercel, Docker)

---

## AI Stack

### Herramientas de IA Utilizadas

Este proyecto fue desarrollado con asistencia de inteligencia artificial:

| Herramienta | Modelo | Uso |
|-------------|--------|-----|
| **Google Gemini CLI / Antigravity** | - | Entorno de desarrollo asistido |
| **Anthropic Claude** | Opus / Sonnet | Generacion de codigo y documentacion |

### Advertencias Importantes

> **NO APTO PARA PRODUCCION**

Este proyecto:

- Es un **MVP educativo**, no una aplicacion lista para produccion
- Puede contener **vulnerabilidades de seguridad** no detectadas
- NO ha sido auditado por profesionales de seguridad
- Esta destinado exclusivamente a:
  - Aprendizaje y ensenanza
  - Desarrollo local
  - Prototipos y demos

**NO desplegar en produccion sin una revision exhaustiva de seguridad.**

---

## Arquitectura

```
Clean Architecture (Simplificada)
|
|-- Presentation (API)     --> Flask routes, middleware
|-- Application (Service)  --> Casos de uso, orquestacion
|-- Domain (Core)          --> Entidades, reglas de negocio
|-- Infrastructure         --> Supabase, configuracion
```

### Patrones de Diseno

- **Repository**: Abstraccion de acceso a datos
- **Factory**: Creacion de servicios con dependencias
- **Singleton**: Cliente Supabase unico
- **Decorator**: Middleware de autenticacion
- **Dependency Injection**: Servicios reciben repositorio

---

## Requisitos

- Python 3.10+
- Cuenta en Supabase (gratis)
- Git

---

## Instalacion Local

### 1. Clonar Repositorio

```bash
git clone https://github.com/cynthiavillagra/pruebadidactica.git
cd pruebadidactica
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
copy .env.example .env
# Editar .env con tus credenciales de Supabase
```

Ver [docs/setup_externo.md](docs/setup_externo.md) para guia detallada.

### 5. Iniciar Servidor

```bash
python api/index.py
```

Abrir http://localhost:5000

---

## Despliegue

### Vercel

```bash
# Instalar Vercel CLI
npm i -g vercel

# Desplegar
vercel

# Configurar variables de entorno en Vercel Dashboard
```

### Docker

```bash
# Construir imagen
docker build -t app-didactica-crud .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env app-didactica-crud
```

---

## Estructura del Proyecto

```
app-prueba-didactica/
|-- api/                    # Capa de presentacion
|   |-- index.py            # Entry point
|   |-- routes.py           # Endpoints REST
|   |-- middleware/         # Autenticacion
|
|-- application/            # Capa de aplicacion
|   |-- alumno_service.py   # Casos de uso
|
|-- domain/                 # Capa de dominio
|   |-- entities/           # Entidades
|   |-- repositories/       # Interfaces
|   |-- exceptions.py       # Excepciones
|
|-- infrastructure/         # Capa de infraestructura
|   |-- config.py           # Configuracion
|   |-- supabase_client.py  # Cliente BD
|   |-- supabase_alumno_repository.py
|
|-- database/               # Scripts SQL
|-- docs/                   # Documentacion
|-- static/                 # Frontend
|-- tests/                  # Pruebas
```

---

## API Endpoints

| Metodo | Endpoint | Descripcion | Auth |
|--------|----------|-------------|------|
| GET | `/api/health` | Health check | No |
| GET | `/api/alumnos` | Listar alumnos | Si |
| POST | `/api/alumnos` | Crear alumno | Si |
| GET | `/api/alumnos/{id}` | Obtener alumno | Si |
| PUT | `/api/alumnos/{id}` | Actualizar alumno | Si |
| DELETE | `/api/alumnos/{id}` | Eliminar alumno | Si |

---

## Documentacion

- [Planificacion y Analisis](docs/01_planificacion_analisis.md)
- [Arquitectura y Patrones](docs/02_a_arquitectura_patrones.md)
- [Modelado de Datos](docs/02_b_modelado_datos.md)
- [Especificacion API](docs/03_c_api_dinamica.md)
- [Manual de Base de Datos](docs/035_manual_bbdd.md)
- [Configuracion APIs Externas](docs/setup_externo.md)

---

## Licencia

Este proyecto esta licenciado bajo **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Puedes:
- Compartir: copiar y redistribuir el material
- Adaptar: remezclar, transformar y construir sobre el material

Ver [LICENSE](LICENSE) para mas detalles.

---

## Autor

Desarrollado con fines educativos.

---

## Contribuciones

Este es un proyecto educativo. Las contribuciones son bienvenidas para mejorar el material didactico.
