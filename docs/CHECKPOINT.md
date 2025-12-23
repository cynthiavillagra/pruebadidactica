# 🔖 CHECKPOINT - Estado del Proyecto

> **Última Actualización**: 2025-12-22 22:17 (UTC-3)  
> **Versión del Documento**: 1.2.0

---

## 📍 Estado Actual

| Campo | Valor |
|-------|-------|
| **Fase Actual** | Fase 3-B - Modelado de Datos ✅ |
| **Sprint** | Sprint 0 (Planificación/Diseño) |
| **Progreso General** | ████░░░░░░ 40% |

---

## 🛠️ Stack Definido

### Backend
| Componente | Tecnología | Versión |
|------------|------------|---------|
| Lenguaje | Python | 3.10+ |
| Framework | Flask | 3.x |
| Cliente BD | supabase-py | 2.x |
| Testing | pytest | 8.x |

### Frontend
| Componente | Tecnología |
|------------|------------|
| Estructura | HTML5 |
| Estilos | CSS3 (Vanilla) |
| Lógica | JavaScript ES6+ |
| Auth SDK | Supabase JS |

### Infraestructura
| Servicio | Proveedor | Tier |
|----------|-----------|------|
| Base de Datos | Supabase (PostgreSQL) | Free |
| Autenticación | Supabase Auth | Free |
| Hosting | Vercel / Local / Docker | Free |

---

## 🏗️ Arquitectura y Modelado Definidos

### Arquitectura
| Aspecto | Decisión |
|---------|----------|
| **Patrón Arquitectónico** | Clean Architecture (Simplificada) |
| **Capas** | Presentación → Aplicación → Dominio ← Infraestructura |
| **Patrones de Diseño** | Repository, DI, Factory, Singleton, Adapter, Decorator |
| **Estado** | Stateless (JWT + Supabase) |

### Modelo de Datos
| Aspecto | Decisión |
|---------|----------|
| **Entidad Principal** | `Alumno` (nombre, apellido, dni) |
| **Identificador** | UUID v4 |
| **Timestamps** | `created_at`, `updated_at` (UTC) |
| **Seguridad BD** | RLS (Row Level Security) |

---

## 📁 Archivos Generados

### Fase 1-2 (Planificación) ✅

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `docs/01_planificacion_analisis.md` | Requisitos, HU, CU, Riesgos | ✅ Completado |
| `.gitignore` | Protección de archivos | ✅ Completado |

### Fase 3-A (Arquitectura) ✅

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `docs/02_a_arquitectura_patrones.md` | Arquitectura, patrones, stateless | ✅ Completado |

### Fase 3-B (Modelado) ✅

| Archivo | Descripción | Estado |
|---------|-------------|--------|
| `docs/02_b_modelado_datos.md` | DER, SQL, Diagrama de clases | ✅ Completado |

### Pendientes (Próximas Fases)

| Archivo | Fase | Estado |
|---------|------|--------|
| `domain/entities/alumno.py` | 4 | ⏳ Pendiente |
| `domain/repositories/alumno_repository.py` | 4 | ⏳ Pendiente |
| `domain/exceptions.py` | 4 | ⏳ Pendiente |
| `infrastructure/supabase_client.py` | 5 | ⏳ Pendiente |
| `infrastructure/supabase_alumno_repository.py` | 5 | ⏳ Pendiente |
| `application/alumno_service.py` | 6 | ⏳ Pendiente |
| `api/routes.py` | 7 | ⏳ Pendiente |
| `api/middleware/auth.py` | 7 | ⏳ Pendiente |
| `static/index.html` | 8 | ⏳ Pendiente |
| `static/css/styles.css` | 8 | ⏳ Pendiente |
| `static/js/app.js` | 8 | ⏳ Pendiente |
| `tests/test_*.py` | 9 | ⏳ Pendiente |
| `Dockerfile` | 10 | ⏳ Pendiente |
| `vercel.json` | 10 | ⏳ Pendiente |

---

## ✅ Decisiones Tomadas

| Decisión | Opción Elegida | Justificación |
|----------|----------------|---------------|
| Framework Backend | Flask | Micro-framework didáctico |
| Base de Datos | Supabase (PostgreSQL) | Gratuito, Auth incluido |
| Frontend | Vanilla JS | Sin build tools |
| Auth Flow | Frontend → Supabase SDK | Backend solo valida JWT |
| Arquitectura | Clean Architecture | Separación de responsabilidades |
| Stateless | Obligatorio | Compatible con serverless |
| ID de Entidades | UUID v4 | Seguro, distribuido |
| Timestamps | UTC | Consistencia global |

---

## 📋 Historial de Commits

| Fecha | Commit | Archivos |
|-------|--------|----------|
| 2025-12-22 | `docs: add initial planning (Phase 1-2)` | `docs/01_planificacion_analisis.md`, `.gitignore` |
| 2025-12-22 | `docs: architecture patterns (Phase 3-A)` | `docs/02_a_arquitectura_patrones.md` |
| 2025-12-22 | `docs: data model and class diagrams (Phase 3-B)` | `docs/02_b_modelado_datos.md` |

---

## 🚀 Siguiente Paso Sugerido

### Fase 4: Implementación de Capa de Dominio

**Tareas a realizar**:
1. Implementar entidad `Alumno` con validaciones
2. Crear interface abstracta del repository (ABC)
3. Definir excepciones de dominio
4. Escribir tests unitarios de la entidad

**Archivos a generar**:
```
domain/
├── __init__.py
├── entities/
│   ├── __init__.py
│   └── alumno.py          # Clase Alumno con validaciones
├── repositories/
│   ├── __init__.py
│   └── alumno_repository.py  # Interface ABC
└── exceptions.py          # Excepciones de dominio

tests/
├── __init__.py
└── test_alumno.py         # Tests de la entidad
```

**Prerequisitos**:
- [x] Planificación completada
- [x] Arquitectura definida
- [x] Modelo de datos definido
- [ ] Aprobación del usuario para continuar

---

## 🔐 Configuración de Entorno

### Variables de Entorno Requeridas

```env
# Supabase (OBLIGATORIO - nunca hardcodear)
SUPABASE_URL=https://[tu-proyecto].supabase.co
SUPABASE_KEY=[tu-anon-key]
SUPABASE_JWT_SECRET=[tu-jwt-secret]

# Flask (opcional para desarrollo)
FLASK_ENV=development
FLASK_DEBUG=1
```

### Verificación de Supabase

- [x] Proyecto creado en Supabase
- [x] Tabla `alumnos` creada con schema
- [ ] RLS (Row Level Security) configurado
- [ ] Variables de entorno configuradas localmente

---

## 🔗 Repositorio Remoto

| Campo | Valor |
|-------|-------|
| **URL** | https://github.com/cynthiavillagra/pruebadidactica |
| **Rama Principal** | `main` |
| **Estado** | ✅ Sincronizado |

---

> **Instrucción**: Actualizar este archivo al completar cada fase.  
> **Formato de commit**: `docs: update checkpoint - fase N completada`
