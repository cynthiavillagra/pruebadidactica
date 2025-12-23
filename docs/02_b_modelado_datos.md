# 📊 Modelado de Datos y Diagrama de Clases

> **Proyecto**: App Didáctica CRUD de Alumnos  
> **Fase**: 3-B (Modelado Estático)  
> **Fecha**: 2025-12-22  
> **Estado**: Pendiente de Aprobación

---

## 📑 Índice

1. [Modelo de Datos Lógico (DER)](#1-modelo-de-datos-lógico-der)
2. [Modelo de Datos Físico (SQL)](#2-modelo-de-datos-físico-sql)
3. [Diagrama de Clases (Backend POO)](#3-diagrama-de-clases-backend-poo)
4. [Diccionario de Datos](#4-diccionario-de-datos)
5. [Mapeo Patrones ↔ Clases](#5-mapeo-patrones--clases)

---

## 1. Modelo de Datos Lógico (DER)

### 1.1 Diagrama Entidad-Relación

Para este MVP, tenemos una única entidad principal: **Alumno**.

```mermaid
erDiagram
    ALUMNO {
        uuid id PK "Identificador único (UUID v4)"
        varchar(100) nombre "Nombre del alumno"
        varchar(100) apellido "Apellido del alumno"
        varchar(20) dni UK "DNI único"
        timestamp created_at "Fecha de creación (UTC)"
        timestamp updated_at "Fecha de última modificación (UTC)"
    }
    
    USUARIO_AUTH {
        uuid id PK "ID de Supabase Auth"
        varchar(255) email UK "Email del usuario"
        timestamp created_at "Fecha de registro"
        timestamp last_sign_in_at "Último login"
    }
    
    USUARIO_AUTH ||--o{ ALUMNO : "gestiona"
```

### 1.2 Descripción del Modelo

| Entidad | Descripción | Responsabilidad |
|---------|-------------|-----------------|
| **ALUMNO** | Entidad principal del sistema | Almacena datos de estudiantes |
| **USUARIO_AUTH** | Manejada por Supabase Auth | Autenticación y sesión (no la creamos nosotros) |

### 1.3 Relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| USUARIO_AUTH → ALUMNO | 1:N (opcional) | Un usuario puede gestionar múltiples alumnos. En este MVP, no hay RLS por usuario (todos ven todo). |

> **📝 Nota sobre USUARIO_AUTH**: Esta tabla es gestionada automáticamente por Supabase Auth. No la creamos ni modificamos directamente; solo consumimos el JWT que genera.

### 1.4 Modelo Extendido (Futuro)

Si en el futuro se requiere trazabilidad de quién creó cada alumno:

```mermaid
erDiagram
    ALUMNO {
        uuid id PK
        varchar(100) nombre
        varchar(100) apellido
        varchar(20) dni UK
        uuid created_by FK "Usuario que creó el registro"
        uuid updated_by FK "Usuario que modificó"
        timestamp created_at
        timestamp updated_at
    }
    
    USUARIO_AUTH {
        uuid id PK
        varchar(255) email UK
    }
    
    USUARIO_AUTH ||--o{ ALUMNO : "created_by"
    USUARIO_AUTH ||--o{ ALUMNO : "updated_by"
```

> ⚠️ Este modelo extendido está **FUERA DEL ALCANCE del MVP**. Se documenta para referencia futura.

---

## 2. Modelo de Datos Físico (SQL)

### 2.1 Script de Creación (Supabase)

```sql
-- ═══════════════════════════════════════════════════════════════
-- MODELO FÍSICO: TABLA ALUMNOS
-- Ejecutar en Supabase SQL Editor
-- ═══════════════════════════════════════════════════════════════

-- Extensión para generar UUIDs (ya viene habilitada en Supabase)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ───────────────────────────────────────────────────────────────
-- TABLA PRINCIPAL: alumnos
-- ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS alumnos (
    -- Clave primaria: UUID generado automáticamente
    -- POR QUÉ UUID: Seguro, no expone cantidad de registros, 
    -- funciona en sistemas distribuidos
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Datos del alumno
    -- POR QUÉ VARCHAR(100): Balance entre flexibilidad y límite razonable
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    
    -- DNI único
    -- POR QUÉ VARCHAR(20): Permite diferentes formatos internacionales
    -- POR QUÉ UNIQUE: Requisito de negocio RF-005
    dni VARCHAR(20) UNIQUE NOT NULL,
    
    -- Timestamps de auditoría
    -- POR QUÉ TIMESTAMP WITH TIME ZONE: Seguridad en zonas horarias
    -- POR QUÉ DEFAULT NOW(): Automático, menos errores humanos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ───────────────────────────────────────────────────────────────
-- ÍNDICES
-- ───────────────────────────────────────────────────────────────

-- Índice para búsqueda por DNI (ya implícito por UNIQUE, pero explícito)
CREATE INDEX IF NOT EXISTS idx_alumnos_dni ON alumnos(dni);

-- Índice para ordenar por apellido (caso de uso más común)
CREATE INDEX IF NOT EXISTS idx_alumnos_apellido ON alumnos(apellido);

-- Índice compuesto para búsqueda por nombre completo
CREATE INDEX IF NOT EXISTS idx_alumnos_nombre_apellido ON alumnos(apellido, nombre);

-- ───────────────────────────────────────────────────────────────
-- TRIGGER: Actualizar updated_at automáticamente
-- ───────────────────────────────────────────────────────────────

-- Función que actualiza el timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    -- POR QUÉ NOW() sin timezone.utc: Supabase maneja UTC internamente
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que ejecuta la función antes de cada UPDATE
DROP TRIGGER IF EXISTS trigger_alumnos_updated_at ON alumnos;
CREATE TRIGGER trigger_alumnos_updated_at
    BEFORE UPDATE ON alumnos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ───────────────────────────────────────────────────────────────
-- COMENTARIOS DE DOCUMENTACIÓN
-- ───────────────────────────────────────────────────────────────

COMMENT ON TABLE alumnos IS 'Tabla principal que almacena datos de estudiantes. Parte del MVP CRUD.';
COMMENT ON COLUMN alumnos.id IS 'Identificador único UUID v4, generado automáticamente.';
COMMENT ON COLUMN alumnos.nombre IS 'Nombre del alumno. Requerido. Máximo 100 caracteres.';
COMMENT ON COLUMN alumnos.apellido IS 'Apellido del alumno. Requerido. Máximo 100 caracteres.';
COMMENT ON COLUMN alumnos.dni IS 'Documento Nacional de Identidad. Único en todo el sistema.';
COMMENT ON COLUMN alumnos.created_at IS 'Timestamp de creación del registro (UTC).';
COMMENT ON COLUMN alumnos.updated_at IS 'Timestamp de última modificación (UTC). Actualizado automáticamente.';
```

### 2.2 Row Level Security (RLS) - Básico

```sql
-- ═══════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS)
-- Protege la tabla a nivel de fila
-- ═══════════════════════════════════════════════════════════════

-- Habilitar RLS en la tabla
ALTER TABLE alumnos ENABLE ROW LEVEL SECURITY;

-- Política: Solo usuarios autenticados pueden ver alumnos
-- POR QUÉ: Previene acceso anónimo a datos
CREATE POLICY "Usuarios autenticados pueden leer alumnos"
    ON alumnos
    FOR SELECT
    TO authenticated
    USING (true);

-- Política: Solo usuarios autenticados pueden insertar
CREATE POLICY "Usuarios autenticados pueden crear alumnos"
    ON alumnos
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Política: Solo usuarios autenticados pueden actualizar
CREATE POLICY "Usuarios autenticados pueden editar alumnos"
    ON alumnos
    FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Política: Solo usuarios autenticados pueden eliminar
CREATE POLICY "Usuarios autenticados pueden eliminar alumnos"
    ON alumnos
    FOR DELETE
    TO authenticated
    USING (true);

-- ───────────────────────────────────────────────────────────────
-- NOTA: En un sistema con múltiples usuarios, se agregaría:
-- USING (created_by = auth.uid())
-- Para que cada usuario solo vea sus propios registros.
-- Esto está FUERA DEL ALCANCE del MVP.
-- ───────────────────────────────────────────────────────────────
```

### 2.3 Datos de Prueba (Opcional)

```sql
-- ═══════════════════════════════════════════════════════════════
-- DATOS DE PRUEBA (Solo para desarrollo)
-- ═══════════════════════════════════════════════════════════════

-- Insertar algunos alumnos de ejemplo
INSERT INTO alumnos (nombre, apellido, dni) VALUES
    ('Juan', 'Pérez', '12345678'),
    ('María', 'González', '23456789'),
    ('Carlos', 'López', '34567890'),
    ('Ana', 'Martínez', '45678901'),
    ('Luis', 'García', '56789012');

-- Verificar inserción
SELECT * FROM alumnos ORDER BY apellido;
```

---

## 3. Diagrama de Clases (Backend POO)

### 3.1 Diagrama Completo del Sistema

Este diagrama refleja todos los patrones definidos en la Fase 3-A:

```mermaid
classDiagram
    direction TB
    
    %% ═══════════════════════════════════════════════════════════
    %% CAPA DE DOMINIO (Núcleo - Sin dependencias externas)
    %% ═══════════════════════════════════════════════════════════
    
    class Alumno {
        <<Entity>>
        -str _id
        -str _nombre
        -str _apellido
        -str _dni
        -datetime _created_at
        -datetime _updated_at
        +__init__(nombre, apellido, dni, id, created_at, updated_at)
        +from_dict(data) Alumno$
        +to_dict() dict
        +validar_nombre(nombre) void
        +validar_apellido(apellido) void
        +validar_dni(dni) void
        +id: str
        +nombre: str
        +apellido: str
        +dni: str
        +nombre_completo: str
    }
    
    class AlumnoRepository {
        <<Interface / ABC>>
        +crear(alumno: Alumno)* Alumno
        +obtener_por_id(id: str)* Optional~Alumno~
        +obtener_por_dni(dni: str)* Optional~Alumno~
        +listar_todos()* List~Alumno~
        +actualizar(alumno: Alumno)* Alumno
        +eliminar(id: str)* bool
        +existe_dni(dni: str, excluir_id: str)* bool
    }
    
    class AlumnoNoEncontrado {
        <<Exception>>
        +message: str
    }
    
    class DNIDuplicado {
        <<Exception>>
        +message: str
    }
    
    class ValidacionError {
        <<Exception>>
        +message: str
        +campo: str
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% CAPA DE APLICACIÓN (Casos de Uso)
    %% ═══════════════════════════════════════════════════════════
    
    class AlumnoService {
        <<Service>>
        -AlumnoRepository _repository
        +__init__(repository: AlumnoRepository)
        +crear_alumno(nombre, apellido, dni) Alumno
        +obtener_alumno(id: str) Alumno
        +listar_alumnos() List~Alumno~
        +actualizar_alumno(id, nombre, apellido, dni) Alumno
        +eliminar_alumno(id: str) bool
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% CAPA DE INFRAESTRUCTURA (Implementaciones Concretas)
    %% ═══════════════════════════════════════════════════════════
    
    class SupabaseClient {
        <<Singleton>>
        -Client _instance$
        -Lock _lock$
        +get_instance()$ Client
    }
    
    class SupabaseAlumnoRepository {
        <<Repository Implementation>>
        -Client _client
        -str _table
        +__init__()
        +crear(alumno: Alumno) Alumno
        +obtener_por_id(id: str) Optional~Alumno~
        +obtener_por_dni(dni: str) Optional~Alumno~
        +listar_todos() List~Alumno~
        +actualizar(alumno: Alumno) Alumno
        +eliminar(id: str) bool
        +existe_dni(dni: str, excluir_id: str) bool
        -_map_to_entity(data: dict) Alumno
        -_map_to_dict(alumno: Alumno) dict
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% CAPA DE PRESENTACIÓN (API)
    %% ═══════════════════════════════════════════════════════════
    
    class FlaskApp {
        <<Controller>>
        +listar_alumnos() Response
        +crear_alumno() Response
        +obtener_alumno(id) Response
        +actualizar_alumno(id) Response
        +eliminar_alumno(id) Response
    }
    
    class AuthMiddleware {
        <<Decorator>>
        +require_auth(func) Callable
        -validar_jwt(token: str) dict
        -extraer_token(header: str) str
    }
    
    class ServiceFactory {
        <<Factory>>
        +create_alumno_service()$ AlumnoService
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% RELACIONES
    %% ═══════════════════════════════════════════════════════════
    
    %% Herencia / Implementación
    SupabaseAlumnoRepository ..|> AlumnoRepository : implements
    
    %% Dependencias (Inyección)
    AlumnoService --> AlumnoRepository : depends on (injected)
    SupabaseAlumnoRepository --> SupabaseClient : uses
    SupabaseAlumnoRepository --> Alumno : creates/maps
    
    %% Uso
    FlaskApp --> AuthMiddleware : uses
    FlaskApp --> ServiceFactory : uses
    ServiceFactory --> AlumnoService : creates
    ServiceFactory --> SupabaseAlumnoRepository : creates
    AlumnoService --> Alumno : manipulates
    
    %% Excepciones
    Alumno ..> ValidacionError : throws
    AlumnoService ..> AlumnoNoEncontrado : throws
    AlumnoService ..> DNIDuplicado : throws
    SupabaseAlumnoRepository ..> AlumnoNoEncontrado : throws
```

### 3.2 Diagrama por Capas (Simplificado)

```mermaid
classDiagram
    direction LR
    
    %% PRESENTACIÓN
    class Presentacion {
        <<Layer>>
        FlaskApp
        AuthMiddleware
        ServiceFactory
    }
    
    %% APLICACIÓN
    class Aplicacion {
        <<Layer>>
        AlumnoService
    }
    
    %% DOMINIO
    class Dominio {
        <<Layer>>
        Alumno
        AlumnoRepository~Interface~
        Exceptions
    }
    
    %% INFRAESTRUCTURA
    class Infraestructura {
        <<Layer>>
        SupabaseAlumnoRepository
        SupabaseClient
    }
    
    %% Flujo de dependencias (hacia adentro)
    Presentacion --> Aplicacion
    Aplicacion --> Dominio
    Infraestructura --> Dominio : implements
    Presentacion --> Infraestructura : creates
```

### 3.3 Diagrama de Secuencia: Crear Alumno

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuario
    participant F as Frontend (JS)
    participant M as AuthMiddleware
    participant R as Routes (Flask)
    participant Fac as ServiceFactory
    participant S as AlumnoService
    participant Rep as SupabaseRepository
    participant DB as Supabase (BD)
    
    U->>F: Completa formulario y click "Guardar"
    F->>F: Validación frontend (campos requeridos)
    
    F->>M: POST /api/alumnos<br/>{nombre, apellido, dni}<br/>Authorization: Bearer JWT
    
    M->>M: Extraer JWT del header
    M->>M: Validar firma y expiración
    
    alt JWT Inválido
        M-->>F: 401 Unauthorized
        F-->>U: "Sesión expirada"
    end
    
    M->>R: Request válido + user info
    R->>Fac: create_alumno_service()
    Fac->>Rep: new SupabaseAlumnoRepository()
    Fac->>S: new AlumnoService(repository)
    Fac-->>R: service instance
    
    R->>S: crear_alumno(nombre, apellido, dni)
    
    S->>S: Crear instancia Alumno
    Note over S: Alumno(nombre, apellido, dni)<br/>Validaciones internas
    
    alt Validación falla
        S-->>R: raise ValidacionError
        R-->>F: 400 Bad Request
        F-->>U: Mostrar error de validación
    end
    
    S->>Rep: existe_dni(dni)
    Rep->>DB: SELECT * WHERE dni = ?
    DB-->>Rep: resultado
    
    alt DNI existe
        Rep-->>S: True
        S-->>R: raise DNIDuplicado
        R-->>F: 409 Conflict
        F-->>U: "DNI ya registrado"
    end
    
    S->>Rep: crear(alumno)
    Rep->>Rep: _map_to_dict(alumno)
    Rep->>DB: INSERT INTO alumnos (...)
    DB-->>Rep: {id, nombre, apellido, dni, ...}
    Rep->>Rep: _map_to_entity(data)
    Rep-->>S: Alumno (con ID)
    
    S-->>R: Alumno creado
    R->>R: alumno.to_dict()
    R-->>F: 201 Created + JSON
    F-->>U: Actualizar tabla + mensaje éxito
```

### 3.4 Detalle de Cada Clase

#### 3.4.1 Entidad: Alumno

```mermaid
classDiagram
    class Alumno {
        <<Entity>>
        
        %% Atributos privados (encapsulación)
        -str _id
        -str _nombre
        -str _apellido
        -str _dni
        -datetime _created_at
        -datetime _updated_at
        
        %% Constructor
        +__init__(nombre: str, apellido: str, dni: str, id: str?, created_at: datetime?, updated_at: datetime?)
        
        %% Factory Method
        +from_dict(data: dict) Alumno$
        
        %% Serialización
        +to_dict() dict
        
        %% Validaciones privadas
        -_validar_nombre(nombre: str) void
        -_validar_apellido(apellido: str) void
        -_validar_dni(dni: str) void
        
        %% Properties (getters)
        +id: str «property»
        +nombre: str «property»
        +apellido: str «property»
        +dni: str «property»
        +created_at: datetime «property»
        +updated_at: datetime «property»
        +nombre_completo: str «property»
        
        %% Métodos de dominio
        +es_nuevo() bool
        +__eq__(other) bool
        +__repr__() str
    }
    
    note for Alumno "PATRÓN: Factory Method\nfrom_dict() crea instancias\ndesde diccionarios\n\nPRINCIPIO: Inmutabilidad\nAtributos privados con properties"
```

#### 3.4.2 Interface: AlumnoRepository

```mermaid
classDiagram
    class AlumnoRepository {
        <<abstract>>
        
        +crear(alumno: Alumno)* Alumno
        +obtener_por_id(id: str)* Optional~Alumno~
        +obtener_por_dni(dni: str)* Optional~Alumno~
        +listar_todos()* List~Alumno~
        +actualizar(alumno: Alumno)* Alumno
        +eliminar(id: str)* bool
        +existe_dni(dni: str, excluir_id: Optional~str~)* bool
    }
    
    note for AlumnoRepository "PATRÓN: Repository\nAbstrae acceso a datos\n\nPRINCIPIO: DIP\nEl servicio depende de\nesta abstracción, no de\nla implementación concreta"
```

#### 3.4.3 Implementación: SupabaseAlumnoRepository

```mermaid
classDiagram
    class SupabaseAlumnoRepository {
        <<concrete>>
        
        -Client _client
        -str _table
        
        +__init__()
        +crear(alumno: Alumno) Alumno
        +obtener_por_id(id: str) Optional~Alumno~
        +obtener_por_dni(dni: str) Optional~Alumno~
        +listar_todos() List~Alumno~
        +actualizar(alumno: Alumno) Alumno
        +eliminar(id: str) bool
        +existe_dni(dni: str, excluir_id: Optional~str~) bool
        
        -_map_to_entity(data: dict) Alumno
        -_map_to_dict(alumno: Alumno) dict
        -_handle_supabase_error(error: Exception) void
    }
    
    class AlumnoRepository {
        <<interface>>
    }
    
    SupabaseAlumnoRepository ..|> AlumnoRepository : implements
    
    note for SupabaseAlumnoRepository "PATRÓN: Adapter\nTraduce API de Supabase\na nuestra interface\n\nPATRÓN: Repository\nImplementación concreta"
```

#### 3.4.4 Servicio: AlumnoService

```mermaid
classDiagram
    class AlumnoService {
        <<service>>
        
        -AlumnoRepository _repository
        
        +__init__(repository: AlumnoRepository)
        +crear_alumno(nombre: str, apellido: str, dni: str) Alumno
        +obtener_alumno(id: str) Alumno
        +listar_alumnos() List~Alumno~
        +actualizar_alumno(id: str, nombre: str, apellido: str, dni: str) Alumno
        +eliminar_alumno(id: str) bool
        
        -_validar_dni_unico(dni: str, excluir_id: Optional~str~) void
    }
    
    class AlumnoRepository {
        <<interface>>
    }
    
    AlumnoService --> AlumnoRepository : uses (injected)
    
    note for AlumnoService "PATRÓN: Dependency Injection\nRecibe repository en constructor\n\nPRINCIPIO: SRP\nSolo orquesta casos de uso"
```

#### 3.4.5 Singleton: SupabaseClient

```mermaid
classDiagram
    class SupabaseClient {
        <<singleton>>
        
        -Client _instance$
        -Lock _lock$
        
        +get_instance()$ Client
        -__init__()
    }
    
    note for SupabaseClient "PATRÓN: Singleton\nUna sola instancia del cliente\n\nThread-safe con Lock\n\nLazy initialization"
```

#### 3.4.6 Factory: ServiceFactory

```mermaid
classDiagram
    class ServiceFactory {
        <<factory>>
        
        +create_alumno_service()$ AlumnoService
    }
    
    class AlumnoService {
        <<service>>
    }
    
    class SupabaseAlumnoRepository {
        <<repository>>
    }
    
    ServiceFactory ..> AlumnoService : creates
    ServiceFactory ..> SupabaseAlumnoRepository : creates
    
    note for ServiceFactory "PATRÓN: Factory\nEncapsula creación de\nobjetos complejos\n\nCentraliza la inyección\nde dependencias"
```

#### 3.4.7 Decorator: AuthMiddleware

```mermaid
classDiagram
    class AuthMiddleware {
        <<decorator>>
        
        +require_auth(func: Callable) Callable
        -_validar_jwt(token: str) dict
        -_extraer_token(header: str) str
    }
    
    note for AuthMiddleware "PATRÓN: Decorator\nAñade autenticación a\nfunciones existentes\n\n@require_auth\ndef mi_ruta(): ..."
```

---

## 4. Diccionario de Datos

### 4.1 Tabla: alumnos

| Campo | Tipo SQL | Tipo Python | Nullable | Default | Descripción |
|-------|----------|-------------|----------|---------|-------------|
| `id` | `UUID` | `str` | NO | `gen_random_uuid()` | Identificador único |
| `nombre` | `VARCHAR(100)` | `str` | NO | - | Nombre del alumno |
| `apellido` | `VARCHAR(100)` | `str` | NO | - | Apellido del alumno |
| `dni` | `VARCHAR(20)` | `str` | NO | - | DNI (único) |
| `created_at` | `TIMESTAMPTZ` | `datetime` | NO | `NOW()` | Fecha creación |
| `updated_at` | `TIMESTAMPTZ` | `datetime` | NO | `NOW()` | Fecha modificación |

### 4.2 Restricciones (Constraints)

| Constraint | Tipo | Campo(s) | Descripción |
|------------|------|----------|-------------|
| `alumnos_pkey` | PRIMARY KEY | `id` | Clave primaria |
| `alumnos_dni_key` | UNIQUE | `dni` | DNI único en todo el sistema |

### 4.3 Índices

| Índice | Campo(s) | Tipo | Propósito |
|--------|----------|------|-----------|
| `idx_alumnos_dni` | `dni` | B-tree | Búsqueda por DNI |
| `idx_alumnos_apellido` | `apellido` | B-tree | Ordenamiento por apellido |
| `idx_alumnos_nombre_apellido` | `apellido, nombre` | B-tree | Búsqueda por nombre completo |

### 4.4 Validaciones de Negocio

| Campo | Regla | Implementación | Capa |
|-------|-------|----------------|------|
| `nombre` | Requerido, 1-100 chars | `Alumno._validar_nombre()` | Dominio |
| `apellido` | Requerido, 1-100 chars | `Alumno._validar_apellido()` | Dominio |
| `dni` | Requerido, único, 1-20 chars | `Alumno._validar_dni()` + BD | Dominio + BD |
| `dni` | No duplicado | `AlumnoService._validar_dni_unico()` | Aplicación |

---

## 5. Mapeo Patrones ↔ Clases

### 5.1 Tabla de Mapeo

| Patrón | Clase(s) | Archivo | Propósito |
|--------|----------|---------|-----------|
| **Repository** | `AlumnoRepository` (interface) | `domain/repositories/alumno_repository.py` | Contrato abstracto |
| **Repository** | `SupabaseAlumnoRepository` (impl) | `infrastructure/supabase_alumno_repository.py` | Implementación Supabase |
| **Factory Method** | `Alumno.from_dict()` | `domain/entities/alumno.py` | Crear entidad desde dict |
| **Singleton** | `SupabaseClient` | `infrastructure/supabase_client.py` | Una conexión a BD |
| **Dependency Injection** | `AlumnoService.__init__(repository)` | `application/alumno_service.py` | Inyectar repository |
| **Factory** | `ServiceFactory` | `api/routes.py` | Crear service con deps |
| **Adapter** | `SupabaseAlumnoRepository` | `infrastructure/supabase_alumno_repository.py` | Adaptar API Supabase |
| **Decorator** | `@require_auth` | `api/middleware/auth.py` | Añadir auth a rutas |

### 5.2 Diagrama de Patrones Aplicados

```mermaid
flowchart TB
    subgraph "PATRONES CREACIONALES"
        SINGLETON["🔷 Singleton<br/>SupabaseClient"]
        FACTORY["🔷 Factory<br/>ServiceFactory"]
        FACTORY_METHOD["🔷 Factory Method<br/>Alumno.from_dict()"]
    end
    
    subgraph "PATRONES ESTRUCTURALES"
        REPOSITORY["🔶 Repository<br/>AlumnoRepository"]
        ADAPTER["🔶 Adapter<br/>SupabaseAlumnoRepository"]
        DECORATOR["🔶 Decorator<br/>@require_auth"]
    end
    
    subgraph "PATRONES DE COMPORTAMIENTO"
        DI["🔷 Dependency Injection<br/>Service(repository)"]
    end
    
    subgraph "CLASES DEL SISTEMA"
        direction TB
        A[Alumno]
        AR[AlumnoRepository<br/>«interface»]
        SAR[SupabaseAlumnoRepository]
        SC[SupabaseClient]
        AS[AlumnoService]
        SF[ServiceFactory]
        AM[AuthMiddleware]
    end
    
    FACTORY_METHOD --> A
    SINGLETON --> SC
    FACTORY --> SF
    REPOSITORY --> AR
    ADAPTER --> SAR
    DI --> AS
    DECORATOR --> AM
    
    SF --> AS
    AS --> AR
    SAR --> SC
    SAR -.-> AR
```

---

## 📊 Resumen del Modelado

### Modelo de Datos

| Aspecto | Decisión |
|---------|----------|
| **Entidad Principal** | `Alumno` (nombre, apellido, DNI) |
| **Identificador** | UUID v4 (seguro, distribuido) |
| **Timestamps** | `created_at`, `updated_at` (UTC) |
| **Constraint Principal** | DNI único |
| **RLS** | Solo usuarios autenticados |

### Clases del Sistema

| Capa | Clases | Patrones |
|------|--------|----------|
| **Dominio** | `Alumno`, `AlumnoRepository` | Factory Method, Repository |
| **Aplicación** | `AlumnoService` | Dependency Injection |
| **Infraestructura** | `SupabaseAlumnoRepository`, `SupabaseClient` | Adapter, Singleton |
| **Presentación** | `FlaskApp`, `AuthMiddleware`, `ServiceFactory` | Decorator, Factory |

---

> **Estado del Documento**: Pendiente de Aprobación  
> **Siguiente Paso**: Implementación de código (Fase 4)
