# 📋 Documento de Planificación y Análisis

> **Proyecto**: App Didáctica CRUD de Alumnos  
> **Versión**: 1.0.0  
> **Fecha de Creación**: 2025-12-22  
> **Autor**: Equipo de Desarrollo  
> **Estado**: Fase 2 - Planificación Completada

---

## 📑 Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Plan de Trabajo (Sprints)](#2-plan-de-trabajo-sprints)
3. [Definición de Requisitos](#3-definición-de-requisitos)
4. [Análisis Funcional Detallado](#4-análisis-funcional-detallado)
5. [Modularización](#5-modularización)
6. [Análisis de Riesgos](#6-análisis-de-riesgos)

---

## 1. Resumen Ejecutivo

### 1.1 Definición del Proyecto

**Nombre**: App Didáctica CRUD de Alumnos

**Descripción**: Aplicación web educativa que implementa un sistema CRUD (Create, Read, Update, Delete) para gestión de datos de alumnos. El proyecto está diseñado como herramienta pedagógica para enseñar desarrollo de software siguiendo Clean Architecture y buenas prácticas de la industria.

**Propósito Dual**:
1. **Funcional**: Gestionar datos de alumnos (nombre, apellido, DNI)
2. **Educativo**: Servir como plantilla documentada para aprender desarrollo ordenado desde cero

### 1.2 Objetivo

| Tipo | Descripción |
|------|-------------|
| **Objetivo Principal** | Desarrollar una aplicación CRUD completa con documentación técnica exhaustiva que sirva como material didáctico para enseñar arquitectura de software |
| **Objetivo Secundario** | Demostrar la implementación de Clean Architecture en Python con despliegue multiplataforma |

### 1.3 Alcance

#### ✅ Dentro del Alcance (IN SCOPE)

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| SC-01 | CRUD Alumnos | Crear, leer, actualizar y eliminar registros |
| SC-02 | Autenticación | Login/logout mediante Supabase Auth |
| SC-03 | Validación | Validación de datos en frontend y backend |
| SC-04 | Persistencia | Almacenamiento en Supabase (PostgreSQL) |
| SC-05 | Despliegue Multi | Compatible con Local, Vercel, Netlify, Docker |
| SC-06 | Documentación | Manual técnico completo con explicaciones |

#### ❌ Fuera del Alcance (OUT OF SCOPE)

| ID | Funcionalidad | Razón de Exclusión |
|----|---------------|-------------------|
| OS-01 | Roles/Permisos | Todos los usuarios tienen los mismos permisos |
| OS-02 | APIs Externas | No se integra con servicios de terceros |
| OS-03 | Reportes/Exportación | No incluido en MVP |
| OS-04 | Notificaciones | No incluido en MVP |
| OS-05 | Auditoría avanzada | Solo timestamps básicos |

### 1.4 Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────────┐
│                      STACK TECNOLÓGICO                          │
├─────────────────────────────────────────────────────────────────┤
│  CAPA          │  TECNOLOGÍA       │  VERSIÓN    │  PROPÓSITO   │
├─────────────────────────────────────────────────────────────────┤
│  Frontend      │  HTML5            │  -          │  Estructura  │
│                │  CSS3             │  -          │  Estilos     │
│                │  JavaScript ES6+  │  -          │  Lógica      │
│                │  Supabase JS SDK  │  2.x        │  Auth + BD   │
├─────────────────────────────────────────────────────────────────┤
│  Backend       │  Python           │  3.10+      │  Lógica      │
│                │  Flask            │  3.x        │  API REST    │
│                │  supabase-py      │  2.x        │  Cliente BD  │
├─────────────────────────────────────────────────────────────────┤
│  Base de Datos │  Supabase         │  -          │  PostgreSQL  │
│                │  (PostgreSQL)     │  15+        │  Persistencia│
├─────────────────────────────────────────────────────────────────┤
│  Auth          │  Supabase Auth    │  -          │  JWT + OAuth │
├─────────────────────────────────────────────────────────────────┤
│  Despliegue    │  Local (Flask)    │  -          │  Desarrollo  │
│                │  Vercel           │  -          │  Serverless  │
│                │  Docker           │  -          │  Contenedor  │
├─────────────────────────────────────────────────────────────────┤
│  Testing       │  pytest           │  8.x        │  Unit tests  │
│                │  pytest-cov       │  -          │  Coverage    │
└─────────────────────────────────────────────────────────────────┘
```

#### Justificación de Elecciones Tecnológicas

| Tecnología | ¿Por qué SÍ? | ¿Por qué NO alternativas? |
|------------|--------------|---------------------------|
| **Flask** | Micro-framework mínimo, ideal para enseñar HTTP sin magia | Django es demasiado opinionado; FastAPI requiere async |
| **Supabase** | PostgreSQL gratis con Auth incluido, panel visual | Firebase es NoSQL (menos didáctico para SQL) |
| **Vanilla JS** | Sin build tools, código transparente | React/Vue agregan complejidad innecesaria para CRUD simple |
| **Python POO** | Lenguaje limpio para enseñar OOP | Java es verboso; Node.js mezcla paradigmas |

---

## 2. Plan de Trabajo (Sprints)

### 2.1 Metodología

- **Framework**: Adaptación de Scrum para proyecto individual/educativo
- **Duración de Sprint**: 1 semana
- **Ceremonias**: Checkpoint al final de cada fase

### 2.2 Roadmap de Sprints

```
SPRINT 0 (Actual)         SPRINT 1                SPRINT 2                SPRINT 3
─────────────────────    ─────────────────────   ─────────────────────   ─────────────────────
│ PLANIFICACIÓN     │    │ BACKEND           │   │ FRONTEND          │   │ PRODUCCIÓN      │
│                   │    │                   │   │                   │   │                 │
│ • Requisitos      │    │ • Domain Layer    │   │ • HTML/CSS        │   │ • Docker        │
│ • Análisis        │    │ • Infrastructure  │   │ • JavaScript      │   │ • Vercel Deploy │
│ • Arquitectura    │    │ • Application     │   │ • Integración     │   │ • Docs Finales  │
│ • Documentación   │    │ • API Layer       │   │ • Testing E2E     │   │ • README        │
│                   │    │ • Unit Tests      │   │                   │   │                 │
└───────────────────┘    └───────────────────┘   └───────────────────┘   └───────────────────┘
     Fase 1-2                 Fase 3-6               Fase 7-8               Fase 9-10
```

### 2.3 Detalle de Sprints

#### Sprint 0: Planificación (Actual)

| ID | Tarea | Entregable | Estado |
|----|-------|------------|--------|
| S0-T1 | Definir requisitos | Este documento | ✅ |
| S0-T2 | Diseñar arquitectura | Diagrama de capas | ✅ |
| S0-T3 | Crear estructura de carpetas | Árbol de directorios | ✅ |
| S0-T4 | Configurar repositorio Git | .gitignore, README base | 🔄 |

#### Sprint 1: Backend Core

| ID | Tarea | Entregable | Estimación |
|----|-------|------------|------------|
| S1-T1 | Implementar entidad Alumno | `domain/entities/alumno.py` | 1h |
| S1-T2 | Crear repository interface | `domain/repositories/alumno_repository.py` | 30min |
| S1-T3 | Implementar Supabase repository | `infrastructure/supabase_alumno_repository.py` | 2h |
| S1-T4 | Crear servicio de aplicación | `application/alumno_service.py` | 1h |
| S1-T5 | Implementar rutas API | `api/routes.py` | 2h |
| S1-T6 | Middleware de autenticación | `api/middleware/auth.py` | 1.5h |
| S1-T7 | Tests unitarios | `tests/test_*.py` | 2h |

#### Sprint 2: Frontend + Integración

| ID | Tarea | Entregable | Estimación |
|----|-------|------------|------------|
| S2-T1 | Crear estructura HTML | `static/index.html` | 1h |
| S2-T2 | Diseñar estilos CSS | `static/css/styles.css` | 2h |
| S2-T3 | Lógica JavaScript CRUD | `static/js/app.js` | 3h |
| S2-T4 | Integrar Supabase Auth | Login/Logout en JS | 2h |
| S2-T5 | Testing de integración | Tests E2E manuales | 1h |

#### Sprint 3: Producción + Documentación

| ID | Tarea | Entregable | Estimación |
|----|-------|------------|------------|
| S3-T1 | Crear Dockerfile | `Dockerfile`, `docker-compose.yml` | 1h |
| S3-T2 | Configurar Vercel | `vercel.json`, handlers | 1h |
| S3-T3 | Deploy a producción | URL funcional | 1h |
| S3-T4 | Manual técnico final | `docs/MANUAL_TECNICO.md` | 3h |
| S3-T5 | README completo | `README.md` | 1h |

---

## 3. Definición de Requisitos

### 3.1 Requisitos Funcionales (MoSCoW)

#### 🔴 MUST HAVE (Obligatorios)

| ID | Requisito | Descripción | Criterio de Aceptación |
|----|-----------|-------------|------------------------|
| RF-001 | Crear alumno | El sistema debe permitir registrar un nuevo alumno | Alumno guardado en BD con ID único |
| RF-002 | Listar alumnos | El sistema debe mostrar todos los alumnos registrados | Lista con nombre, apellido, DNI visible |
| RF-003 | Editar alumno | El sistema debe permitir modificar datos de un alumno | Cambios reflejados en BD inmediatamente |
| RF-004 | Eliminar alumno | El sistema debe permitir borrar un alumno | Registro eliminado de BD |
| RF-005 | Validar DNI único | El sistema debe rechazar DNI duplicados | Error visible si DNI ya existe |
| RF-006 | Autenticar usuario | El sistema debe requerir login para operar | Redirección a login si no autenticado |
| RF-007 | Cerrar sesión | El sistema debe permitir logout | Sesión terminada, JWT invalidado |

#### 🟡 SHOULD HAVE (Importantes)

| ID | Requisito | Descripción | Criterio de Aceptación |
|----|-----------|-------------|------------------------|
| RF-008 | Buscar alumno | Filtrar lista por nombre o DNI | Resultados filtrados en tiempo real |
| RF-009 | Confirmar eliminación | Pedir confirmación antes de borrar | Modal de confirmación visible |
| RF-010 | Mensajes de feedback | Mostrar éxito/error en operaciones | Toast/Alert visible por 3 segundos |

#### 🟢 COULD HAVE (Deseables)

| ID | Requisito | Descripción | Criterio de Aceptación |
|----|-----------|-------------|------------------------|
| RF-011 | Ordenar lista | Ordenar por columna (nombre, apellido) | Click en header ordena lista |
| RF-012 | Paginación | Mostrar resultados paginados | 10 registros por página |

#### ⚪ WON'T HAVE (Excluidos de MVP)

| ID | Requisito | Razón de Exclusión |
|----|-----------|-------------------|
| RF-013 | Exportar a Excel | Fuera de alcance MVP |
| RF-014 | Importar desde CSV | Fuera de alcance MVP |
| RF-015 | Historial de cambios | Complejidad innecesaria para didáctica |

### 3.2 Requisitos No Funcionales

| ID | Categoría | Requisito | Métrica |
|----|-----------|-----------|---------|
| RNF-001 | **Seguridad** | No hardcodear credenciales | 0 secrets en código |
| RNF-002 | **Seguridad** | Validar JWT en cada request | 100% endpoints protegidos |
| RNF-003 | **Seguridad** | Timeout de sesión por inactividad | 15 minutos máximo |
| RNF-004 | **Portabilidad** | Funcionar en local, Vercel, Docker | 3 entornos validados |
| RNF-005 | **Stateless** | Sin estado en memoria del servidor | 0 variables globales mutables |
| RNF-006 | **Rendimiento** | Respuesta API < 500ms | Promedio en condiciones normales |
| RNF-007 | **Mantenibilidad** | Cobertura de tests > 70% | pytest-cov |
| RNF-008 | **Documentación** | Cada archivo documentado | 100% archivos con docstrings |
| RNF-009 | **Accesibilidad** | HTML semántico básico | Navegable con teclado |
| RNF-010 | **Fechas** | Usar UTC para timestamps | `datetime.now(timezone.utc)` |

---

## 4. Análisis Funcional Detallado

### 4.1 Historias de Usuario

#### HU-001: Registrar Alumno

```
COMO usuario autenticado
QUIERO registrar un nuevo alumno con nombre, apellido y DNI
PARA mantener un registro de los estudiantes

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que estoy en la pantalla principal
   CUANDO completo el formulario con datos válidos y presiono "Guardar"
   ENTONCES el alumno aparece en la lista y veo un mensaje de éxito

✅ DADO que ingreso un DNI que ya existe
   CUANDO presiono "Guardar"
   ENTONCES veo un mensaje de error "DNI ya registrado"

✅ DADO que dejo campos obligatorios vacíos
   CUANDO presiono "Guardar"
   ENTONCES veo validación en los campos requeridos

NOTAS TÉCNICAS:
• Validación frontend: campos requeridos, formato DNI
• Validación backend: unicidad DNI, sanitización
• Mapping: RF-001, RF-005
```

#### HU-002: Ver Lista de Alumnos

```
COMO usuario autenticado
QUIERO ver la lista de todos los alumnos
PARA conocer los estudiantes registrados

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que accedo a la pantalla principal
   CUANDO la página carga
   ENTONCES veo una tabla con todos los alumnos (nombre, apellido, DNI)

✅ DADO que no hay alumnos registrados
   CUANDO la página carga
   ENTONCES veo un mensaje "No hay alumnos registrados"

NOTAS TÉCNICAS:
• Endpoint: GET /api/alumnos
• Orden por defecto: apellido ASC
• Mapping: RF-002
```

#### HU-003: Editar Alumno

```
COMO usuario autenticado
QUIERO modificar los datos de un alumno existente
PARA corregir errores o actualizar información

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que hago clic en "Editar" en un alumno
   CUANDO se abre el formulario
   ENTONCES veo los datos actuales precargados

✅ DADO que modifico los datos y presiono "Guardar"
   CUANDO la operación es exitosa
   ENTONCES veo los cambios reflejados en la lista

✅ DADO que cambio el DNI a uno que ya existe
   CUANDO presiono "Guardar"
   ENTONCES veo error "DNI ya registrado por otro alumno"

NOTAS TÉCNICAS:
• Endpoint: PUT /api/alumnos/{id}
• Validar que el DNI no pertenezca a OTRO alumno (excluir self)
• Mapping: RF-003, RF-005
```

#### HU-004: Eliminar Alumno

```
COMO usuario autenticado
QUIERO eliminar un alumno del sistema
PARA remover registros incorrectos o dados de baja

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que hago clic en "Eliminar" en un alumno
   CUANDO aparece el modal de confirmación
   ENTONCES puedo confirmar o cancelar la acción

✅ DADO que confirmo la eliminación
   CUANDO la operación es exitosa
   ENTONCES el alumno desaparece de la lista

✅ DADO que cancelo la eliminación
   CUANDO cierro el modal
   ENTONCES el alumno permanece en la lista

NOTAS TÉCNICAS:
• Endpoint: DELETE /api/alumnos/{id}
• Soft delete vs Hard delete: Hard delete (MVP)
• Mapping: RF-004, RF-009
```

#### HU-005: Autenticarse

```
COMO visitante
QUIERO iniciar sesión con mi cuenta
PARA acceder a las funcionalidades del sistema

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que accedo a la aplicación sin sesión
   CUANDO la página carga
   ENTONCES soy redirigido al formulario de login

✅ DADO que ingreso credenciales válidas
   CUANDO presiono "Iniciar Sesión"
   ENTONCES accedo a la pantalla principal

✅ DADO que ingreso credenciales inválidas
   CUANDO presiono "Iniciar Sesión"
   ENTONCES veo error "Credenciales incorrectas"

NOTAS TÉCNICAS:
• Proveedor: Supabase Auth (email/password o magic link)
• Token: JWT almacenado en localStorage
• Mapping: RF-006
```

#### HU-006: Cerrar Sesión

```
COMO usuario autenticado
QUIERO cerrar mi sesión
PARA proteger mi cuenta en dispositivos compartidos

CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────────────────────────
✅ DADO que hago clic en "Cerrar Sesión"
   CUANDO la operación completa
   ENTONCES soy redirigido al login

✅ DADO que intento acceder a la app después de logout
   CUANDO la página carga
   ENTONCES debo autenticarme nuevamente

NOTAS TÉCNICAS:
• Limpiar JWT de localStorage
• Llamar supabase.auth.signOut()
• Mapping: RF-007
```

### 4.2 Casos de Uso (Formato Estricto)

#### CU-001: Gestionar Alumno (CRUD)

```
╔══════════════════════════════════════════════════════════════════╗
║                    CASO DE USO: CU-001                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Nombre:        Gestionar Alumno (CRUD)                           ║
║ Actor:         Usuario Autenticado                               ║
║ Precondición:  Usuario ha iniciado sesión válida                 ║
║ Postcondición: Datos de alumno creados/modificados/eliminados    ║
║ Trigger:       Usuario accede a la pantalla principal            ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO PRINCIPAL (Crear Alumno):                                   ║
╠══════════════════════════════════════════════════════════════════╣
║ 1. Sistema muestra formulario vacío y lista de alumnos           ║
║ 2. Usuario completa campos: nombre, apellido, DNI                ║
║ 3. Usuario presiona botón "Guardar"                              ║
║ 4. Sistema valida datos en frontend                              ║
║ 5. Sistema envía petición POST /api/alumnos                      ║
║ 6. Backend valida JWT y datos                                    ║
║ 7. Backend inserta registro en Supabase                          ║
║ 8. Sistema muestra mensaje de éxito                              ║
║ 9. Sistema actualiza lista de alumnos                            ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO ALTERNATIVO A (Editar Alumno):                             ║
╠══════════════════════════════════════════════════════════════════╣
║ A1. Usuario hace clic en "Editar" de un alumno existente         ║
║ A2. Sistema carga datos en el formulario                         ║
║ A3. Usuario modifica campos deseados                             ║
║ A4. Usuario presiona "Guardar"                                   ║
║ A5. Sistema envía PUT /api/alumnos/{id}                          ║
║ A6. Continúa desde paso 6 del flujo principal                    ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO ALTERNATIVO B (Eliminar Alumno):                           ║
╠══════════════════════════════════════════════════════════════════╣
║ B1. Usuario hace clic en "Eliminar" de un alumno                 ║
║ B2. Sistema muestra modal de confirmación                        ║
║ B3. Usuario confirma eliminación                                 ║
║ B4. Sistema envía DELETE /api/alumnos/{id}                       ║
║ B5. Backend elimina registro                                     ║
║ B6. Sistema actualiza lista (alumno desaparece)                  ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO DE EXCEPCIÓN E1 (DNI Duplicado):                           ║
╠══════════════════════════════════════════════════════════════════╣
║ E1.1 En paso 7, backend detecta DNI existente                    ║
║ E1.2 Backend retorna error 409 Conflict                          ║
║ E1.3 Sistema muestra "El DNI ya está registrado"                 ║
║ E1.4 Formulario permanece con datos para corrección              ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO DE EXCEPCIÓN E2 (Sesión Expirada):                         ║
╠══════════════════════════════════════════════════════════════════╣
║ E2.1 En paso 6, JWT es inválido o expirado                       ║
║ E2.2 Backend retorna error 401 Unauthorized                      ║
║ E2.3 Sistema redirige a pantalla de login                        ║
║ E2.4 Sistema muestra "Sesión expirada, ingrese nuevamente"       ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-002: Autenticar Usuario

```
╔══════════════════════════════════════════════════════════════════╗
║                    CASO DE USO: CU-002                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Nombre:        Autenticar Usuario                                ║
║ Actor:         Visitante (usuario no autenticado)                ║
║ Precondición:  Usuario tiene cuenta registrada en Supabase       ║
║ Postcondición: Usuario autenticado con JWT válido                ║
║ Trigger:       Usuario accede a la aplicación                    ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO PRINCIPAL (Login con Email/Password):                      ║
╠══════════════════════════════════════════════════════════════════╣
║ 1. Sistema detecta ausencia de JWT válido en localStorage        ║
║ 2. Sistema muestra formulario de login                           ║
║ 3. Usuario ingresa email y contraseña                            ║
║ 4. Usuario presiona "Iniciar Sesión"                             ║
║ 5. Frontend llama supabase.auth.signInWithPassword()             ║
║ 6. Supabase valida credenciales y retorna JWT                    ║
║ 7. Frontend almacena JWT en localStorage                         ║
║ 8. Sistema redirige a pantalla principal                         ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO ALTERNATIVO A (Logout):                                    ║
╠══════════════════════════════════════════════════════════════════╣
║ A1. Usuario autenticado presiona "Cerrar Sesión"                 ║
║ A2. Frontend llama supabase.auth.signOut()                       ║
║ A3. Frontend elimina JWT de localStorage                         ║
║ A4. Sistema redirige a pantalla de login                         ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO DE EXCEPCIÓN E1 (Credenciales Inválidas):                  ║
╠══════════════════════════════════════════════════════════════════╣
║ E1.1 En paso 6, Supabase rechaza credenciales                    ║
║ E1.2 Sistema muestra "Email o contraseña incorrectos"            ║
║ E1.3 Formulario permanece para reintento                         ║
╠══════════════════════════════════════════════════════════════════╣
║ FLUJO DE EXCEPCIÓN E2 (Timeout por Inactividad):                 ║
╠══════════════════════════════════════════════════════════════════╣
║ E2.1 Sistema detecta 15 min sin actividad                        ║
║ E2.2 Sistema ejecuta logout automático                           ║
║ E2.3 Sistema muestra "Sesión cerrada por inactividad"            ║
╚══════════════════════════════════════════════════════════════════╝
```

### 4.3 Matriz de Trazabilidad

| Historia de Usuario | Caso de Uso | Requisitos Funcionales | Requisitos No Funcionales |
|---------------------|-------------|------------------------|---------------------------|
| HU-001 | CU-001 | RF-001, RF-005, RF-010 | RNF-001, RNF-002 |
| HU-002 | CU-001 | RF-002 | RNF-006 |
| HU-003 | CU-001 | RF-003, RF-005, RF-010 | RNF-001, RNF-002 |
| HU-004 | CU-001 | RF-004, RF-009, RF-010 | RNF-001, RNF-002 |
| HU-005 | CU-002 | RF-006 | RNF-002, RNF-003 |
| HU-006 | CU-002 | RF-007 | RNF-003 |

---

## 5. Modularización

### 5.1 Módulos Lógicos del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULOS DEL SISTEMA                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MÓDULO: AUTH (Autenticación)                │   │
│  │  Responsabilidad: Gestionar identidad de usuarios        │   │
│  │  Requisitos: RF-006, RF-007                              │   │
│  │  Componentes:                                            │   │
│  │    • Login (frontend: Supabase SDK)                      │   │
│  │    • Logout (frontend: Supabase SDK)                     │   │
│  │    • Middleware JWT (backend: validación)                │   │
│  │    • Watchdog inactividad (frontend: timer)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MÓDULO: ALUMNOS (Core Domain)               │   │
│  │  Responsabilidad: Gestionar entidad Alumno               │   │
│  │  Requisitos: RF-001, RF-002, RF-003, RF-004, RF-005      │   │
│  │  Componentes:                                            │   │
│  │    • Entidad Alumno (domain/entities/)                   │   │
│  │    • Repository Interface (domain/repositories/)         │   │
│  │    • Supabase Repository (infrastructure/)               │   │
│  │    • Alumno Service (application/)                       │   │
│  │    • API Endpoints (api/)                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MÓDULO: UI (Interfaz de Usuario)            │   │
│  │  Responsabilidad: Presentar datos e interacción          │   │
│  │  Requisitos: RF-008, RF-009, RF-010, RF-011, RF-012      │   │
│  │  Componentes:                                            │   │
│  │    • HTML Structure (static/index.html)                  │   │
│  │    • Styles (static/css/styles.css)                      │   │
│  │    • App Logic (static/js/app.js)                        │   │
│  │    • Form Handling                                       │   │
│  │    • Table Rendering                                     │   │
│  │    • Modals & Feedback                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Dependencias entre Módulos

```
        AUTH                    ALUMNOS                    UI
         │                         │                        │
         │   (provee JWT)          │    (provee datos)      │
         └────────────────────────►│◄───────────────────────┘
                                   │                        │
                                   │   (consume API)        │
                                   └────────────────────────┘
```

**Regla de Dependencia**:
- UI depende de AUTH y ALUMNOS
- ALUMNOS depende de AUTH (para validación)
- AUTH no depende de ningún otro módulo (es independiente)

---

## 6. Análisis de Riesgos

### 6.1 Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Nivel | Mitigación |
|----|--------|--------------|---------|-------|------------|
| R-001 | **Memoria Volátil en Serverless** | ALTA | ALTO | 🔴 CRÍTICO | Arquitectura 100% stateless; sin variables globales mutables; estado solo en BD/JWT |
| R-002 | Credenciales expuestas en código | MEDIA | ALTO | 🔴 CRÍTICO | Variables de entorno (`os.getenv`); `.env` en `.gitignore`; nunca hardcodear |
| R-003 | JWT expirado no detectado | MEDIA | MEDIO | 🟡 ALTO | Validar JWT en cada request; manejar 401 en frontend |
| R-004 | Sesión zombie (usuario abandona) | MEDIA | BAJO | 🟡 ALTO | Watchdog de inactividad (15 min); auto-logout |
| R-005 | DNI duplicado race condition | BAJA | MEDIO | 🟢 MEDIO | Constraint UNIQUE en BD; validación backend obligatoria |
| R-006 | Fallo de Supabase | BAJA | ALTO | 🟢 MEDIO | Manejo de errores; mensajes amigables; retry logic opcional |
| R-007 | Incompatibilidad entre entornos | MEDIA | MEDIO | 🟡 ALTO | Tests en local + Docker + Vercel antes de cada release |
| R-008 | Inyección SQL/XSS | BAJA | ALTO | 🟢 MEDIO | Supabase usa queries parametrizadas; sanitizar inputs en frontend |

### 6.2 Plan de Mitigación Detallado

#### 🔴 R-001: Memoria Volátil en Serverless (CRÍTICO)

**Problema**: Vercel/Netlify ejecutan funciones serverless que se destruyen después de cada request. Cualquier dato en RAM se pierde.

**Por qué es crítico**: Si guardamos estado en variables globales (ej: `usuarios_logueados = {}`), funcionará en local pero fallará en producción.

**Mitigación implementada**:
```python
# ❌ PROHIBIDO - Variable global mutable
session_cache = {}  # Se pierde entre requests en serverless

# ✅ CORRECTO - Estado en JWT/BD
def get_current_user(request):
    token = request.headers.get('Authorization')
    return validate_jwt(token)  # Estado viene del token, no de RAM
```

**Checklist de validación**:
- [ ] Ninguna variable global mutable en backend
- [ ] Todo estado en JWT (cliente) o Supabase (servidor)
- [ ] Funciona igual en local y Vercel

#### 🔴 R-002: Credenciales Expuestas (CRÍTICO)

**Mitigación**:
```python
# ❌ PROHIBIDO
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJI..."

# ✅ CORRECTO
import os
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
```

**Archivo `.env.example`** (sin valores reales):
```env
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
```

#### 🟡 R-004: Watchdog de Inactividad

**Implementación frontend**:
```javascript
// Cerrar sesión automáticamente tras 15 min de inactividad
const INACTIVITY_TIMEOUT = 15 * 60 * 1000; // 15 minutos
let inactivityTimer;

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
        supabase.auth.signOut();
        alert('Sesión cerrada por inactividad');
        location.reload();
    }, INACTIVITY_TIMEOUT);
}

// Resetear timer con cualquier actividad
['click', 'keypress', 'scroll', 'mousemove'].forEach(event => {
    document.addEventListener(event, resetInactivityTimer);
});
```

### 6.3 Criterios de Aceptación de Riesgos

| Criterio | Métrica | Estado |
|----------|---------|--------|
| Zero hardcoded secrets | grep de patterns sensibles = 0 | Pendiente |
| Stateless compliance | 0 variables globales mutables | Pendiente |
| JWT validation | 100% endpoints protegidos | Pendiente |
| Inactivity logout | Timer funcional en frontend | Pendiente |

---

## 📎 Anexos

### A. Glosario Técnico

| Término | Definición |
|---------|------------|
| **JWT** | JSON Web Token - Token firmado que contiene información del usuario |
| **Stateless** | Arquitectura sin estado en servidor; cada request es independiente |
| **Clean Architecture** | Patrón que separa dominio, aplicación e infraestructura |
| **MoSCoW** | Priorización: Must/Should/Could/Won't have |
| **Repository Pattern** | Abstracción que oculta detalles de persistencia |
| **CRUD** | Create, Read, Update, Delete - operaciones básicas de datos |

### B. Referencias

- [Supabase Documentation](https://supabase.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

---

> **Documento generado**: 2025-12-22  
> **Próxima revisión**: Al completar Sprint 1  
> **Estado**: ✅ APROBADO PARA DESARROLLO
