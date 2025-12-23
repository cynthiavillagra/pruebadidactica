# 🏗️ Arquitectura y Patrones de Diseño

> **Proyecto**: App Didáctica CRUD de Alumnos  
> **Fase**: 3-A (Arquitectura)  
> **Fecha**: 2025-12-22  
> **Estado**: Pendiente de Aprobación

---

## 📑 Índice

1. [Definición de Arquitectura](#1-definición-de-arquitectura)
2. [Patrones de Diseño (Diccionario)](#2-patrones-de-diseño-diccionario)
3. [Estrategia de Integración (APIs)](#3-estrategia-de-integración-apis)
4. [Estrategia Stateless](#4-estrategia-stateless)
5. [Estructura de Carpetas Detallada](#5-estructura-de-carpetas-detallada)

---

## 1. Definición de Arquitectura

### 1.1 Arquitectura Elegida: Clean Architecture (Simplificada)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                          CLEAN ARCHITECTURE                                 │
│                     (Arquitectura Limpia / Hexagonal)                       │
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────┐     │
│    │                     CAPA DE PRESENTACIÓN                        │     │
│    │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │     │
│    │  │   Frontend      │  │   API Routes    │  │   Middleware   │  │     │
│    │  │   (HTML/JS)     │  │   (Flask)       │  │   (Auth JWT)   │  │     │
│    │  └────────┬────────┘  └────────┬────────┘  └───────┬────────┘  │     │
│    └───────────┼────────────────────┼───────────────────┼───────────┘     │
│                │                    │                   │                  │
│                ▼                    ▼                   ▼                  │
│    ┌─────────────────────────────────────────────────────────────────┐     │
│    │                     CAPA DE APLICACIÓN                          │     │
│    │  ┌─────────────────────────────────────────────────────────┐   │     │
│    │  │                   AlumnoService                          │   │     │
│    │  │   (Casos de Uso / Lógica de Aplicación)                 │   │     │
│    │  └────────────────────────┬────────────────────────────────┘   │     │
│    └───────────────────────────┼────────────────────────────────────┘     │
│                                │                                          │
│                                ▼                                          │
│    ┌─────────────────────────────────────────────────────────────────┐     │
│    │                       CAPA DE DOMINIO                           │     │
│    │  ┌─────────────────┐  ┌─────────────────────────────────────┐  │     │
│    │  │   Alumno        │  │   AlumnoRepository (Interface)      │  │     │
│    │  │   (Entidad)     │  │   (Contrato Abstracto)              │  │     │
│    │  └─────────────────┘  └─────────────────────────────────────┘  │     │
│    └─────────────────────────────────────────────────────────────────┘     │
│                                │                                          │
│                                ▼                                          │
│    ┌─────────────────────────────────────────────────────────────────┐     │
│    │                   CAPA DE INFRAESTRUCTURA                       │     │
│    │  ┌─────────────────────────────────────────────────────────┐   │     │
│    │  │              SupabaseAlumnoRepository                    │   │     │
│    │  │   (Implementación Concreta del Repositorio)             │   │     │
│    │  └────────────────────────┬────────────────────────────────┘   │     │
│    └───────────────────────────┼────────────────────────────────────┘     │
│                                │                                          │
│                                ▼                                          │
│                    ┌─────────────────────┐                                │
│                    │      SUPABASE       │                                │
│                    │   (PostgreSQL)      │                                │
│                    └─────────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Justificación: ¿Por Qué SÍ Clean Architecture?

| Aspecto | ¿Por qué SÍ Clean Architecture? | ¿Por qué NO otras alternativas? |
|---------|----------------------------------|----------------------------------|
| **Separación de Responsabilidades** | Cada capa tiene una única responsabilidad. El dominio no conoce la base de datos. | MVC tradicional mezcla lógica de negocio con acceso a datos |
| **Testabilidad** | Puedo testear el dominio sin tocar la BD real (mocks/stubs) | Código acoplado requiere BD real para tests |
| **Independencia de Frameworks** | Si mañana cambio Flask por FastAPI, solo cambio la capa de presentación | Frameworks invasivos atan el código a su estructura |
| **Independencia de BD** | Si migro de Supabase a Firebase, solo cambio la implementación del repository | Queries directas en servicios = refactoring masivo |
| **Didáctica** | Enseña separation of concerns desde el día 1 | Código "todo junto" enseña malos hábitos |
| **Escalabilidad** | Agregar nuevas entidades sigue el mismo patrón probado | Código espagueti se vuelve imposible de mantener |

### 1.3 Regla de Dependencia

```
                         REGLA DE ORO
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Las dependencias SIEMPRE apuntan hacia ADENTRO.
    Las capas internas NO conocen a las capas externas.
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    EXTERNO ──────────────────────────────► INTERNO
    
    Presentación → Aplicación → Dominio ← Infraestructura
    (Flask)        (Service)    (Entity)   (Supabase)
                                   │
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                        ▼                     ▼
                   NO conoce             Implementa
                   Flask ni              la Interface
                   Supabase              del Dominio
```

**Traducción práctica**:
- `Alumno` (entidad) NO importa `flask` ni `supabase`
- `AlumnoRepository` (interface) NO importa implementaciones concretas
- `SupabaseAlumnoRepository` SÍ importa `supabase` y la interface
- `AlumnoService` SÍ conoce al dominio, pero NO a la infraestructura

### 1.4 Flujo de una Petición (Request Flow)

```
                            FLUJO: CREAR ALUMNO
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  1. USUARIO                                                                  │
│     │                                                                        │
│     │ POST /api/alumnos {"nombre": "Juan", "apellido": "Pérez", "dni": "X"}  │
│     ▼                                                                        │
│  2. MIDDLEWARE (auth.py)                                                     │
│     │                                                                        │
│     │ Valida JWT → Si inválido: 401 Unauthorized                            │
│     ▼                                                                        │
│  3. ROUTES (routes.py)                                                       │
│     │                                                                        │
│     │ Parsea JSON → Llama al Service                                        │
│     ▼                                                                        │
│  4. SERVICE (alumno_service.py)                                              │
│     │                                                                        │
│     │ Crea instancia de Alumno → Valida entidad → Llama al Repository       │
│     ▼                                                                        │
│  5. REPOSITORY INTERFACE (alumno_repository.py)                              │
│     │                                                                        │
│     │ Define contrato abstracto: crear(alumno) → Alumno                     │
│     ▼                                                                        │
│  6. SUPABASE REPOSITORY (supabase_alumno_repository.py)                      │
│     │                                                                        │
│     │ INSERT INTO alumnos (...) → Retorna Alumno creado                     │
│     ▼                                                                        │
│  7. RESPUESTA                                                                │
│     │                                                                        │
│     │ JSON {"id": "uuid", "nombre": "Juan", ...} + 201 Created              │
│     ▼                                                                        │
│  8. USUARIO                                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Patrones de Diseño (Diccionario)

### 2.1 Catálogo de Patrones a Implementar

| Patrón | Categoría | Archivo(s) | Propósito |
|--------|-----------|------------|-----------|
| **Repository** | Estructural | `domain/repositories/`, `infrastructure/` | Abstraer acceso a datos |
| **Dependency Injection** | Creacional | `application/`, `api/` | Desacoplar dependencias |
| **Factory Method** | Creacional | `domain/entities/alumno.py` | Crear entidades válidas |
| **Singleton** | Creacional | `infrastructure/supabase_client.py` | Una sola conexión a BD |
| **Adapter** | Estructural | `infrastructure/` | Adaptar Supabase a nuestra interface |
| **Strategy** | Comportamental | Extensible | Diferentes validaciones/exports |
| **Decorator** | Estructural | `api/middleware/auth.py` | Añadir auth a rutas |

---

### 2.2 Detalle de Cada Patrón

#### 🔷 REPOSITORY PATTERN

**Propósito**: Abstraer el acceso a datos detrás de una interface, permitiendo cambiar la implementación sin tocar la lógica de negocio.

**¿Por qué SÍ?**
- Testeable: Puedo usar un `FakeRepository` en tests
- Desacoplado: El servicio no conoce Supabase
- Sustituible: Puedo migrar a otra BD sin cambiar el dominio

**¿Por qué NO SQL directo en servicios?**
- Acopla la lógica de negocio a la BD específica
- Hace imposible testear sin BD real
- Viola el principio de responsabilidad única

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: REPOSITORY PATTERN
# ═══════════════════════════════════════════════════════════════

# 1. INTERFACE (domain/repositories/alumno_repository.py)
# ───────────────────────────────────────────────────────────────
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.alumno import Alumno

class AlumnoRepository(ABC):
    """
    Contrato abstracto para acceso a datos de Alumno.
    
    POR QUÉ INTERFACE:
    - Define QUÉ operaciones existen, no CÓMO se implementan
    - Permite múltiples implementaciones (Supabase, SQLite, Mock)
    - El dominio depende de la abstracción, no del concreto
    """
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """Persiste un nuevo alumno y retorna el alumno con ID asignado."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Alumno]:
        """Busca alumno por ID. Retorna None si no existe."""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Alumno]:
        """Retorna todos los alumnos."""
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza un alumno existente."""
        pass
    
    @abstractmethod
    def eliminar(self, id: str) -> bool:
        """Elimina un alumno. Retorna True si se eliminó."""
        pass
    
    @abstractmethod
    def existe_dni(self, dni: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si un DNI ya existe (excluyendo un ID opcional)."""
        pass


# 2. IMPLEMENTACIÓN CONCRETA (infrastructure/supabase_alumno_repository.py)
# ───────────────────────────────────────────────────────────────
from domain.repositories.alumno_repository import AlumnoRepository
from domain.entities.alumno import Alumno
from infrastructure.supabase_client import get_supabase_client

class SupabaseAlumnoRepository(AlumnoRepository):
    """
    Implementación del repositorio usando Supabase.
    
    POR QUÉ AQUÍ Y NO EN DOMINIO:
    - El dominio es puro, sin dependencias externas
    - Esta clase conoce Supabase, pero el servicio no
    - Puedo crear otra implementación (SQLite, Mock) sin tocar el servicio
    """
    
    def __init__(self):
        self._client = get_supabase_client()
        self._table = "alumnos"
    
    def crear(self, alumno: Alumno) -> Alumno:
        # Implementación específica de Supabase
        data = {
            "nombre": alumno.nombre,
            "apellido": alumno.apellido,
            "dni": alumno.dni
        }
        response = self._client.table(self._table).insert(data).execute()
        return Alumno.from_dict(response.data[0])
    
    # ... otros métodos
```

---

#### 🔷 DEPENDENCY INJECTION (Inyección de Dependencias)

**Propósito**: Las dependencias se "inyectan" desde afuera en lugar de crearse internamente.

**¿Por qué SÍ?**
- Testeable: Inyecto un mock en tests
- Flexible: Cambio implementaciones sin modificar código
- Explícito: Las dependencias son visibles en el constructor

**¿Por qué NO crear dependencias internas?**
- Oculta dependencias
- Imposible de mockear
- Acoplamiento fuerte

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: DEPENDENCY INJECTION
# ═══════════════════════════════════════════════════════════════

# ❌ MAL: Dependencia creada internamente (acoplado)
class AlumnoServiceMalo:
    def __init__(self):
        # El servicio CREA su propia dependencia
        # No puedo cambiarla, no puedo mockearla
        self.repository = SupabaseAlumnoRepository()

# ✅ BIEN: Dependencia inyectada (desacoplado)
class AlumnoService:
    """
    Servicio de aplicación para operaciones con Alumnos.
    
    POR QUÉ INYECCIÓN:
    - El servicio recibe el repository, no lo crea
    - En producción: inyecto SupabaseAlumnoRepository
    - En tests: inyecto FakeAlumnoRepository
    """
    
    def __init__(self, repository: AlumnoRepository):
        # Depende de la INTERFACE, no de la implementación
        self._repository = repository
    
    def crear_alumno(self, nombre: str, apellido: str, dni: str) -> Alumno:
        # Usa el repository inyectado, sin saber cuál es
        alumno = Alumno(nombre=nombre, apellido=apellido, dni=dni)
        return self._repository.crear(alumno)


# USO EN PRODUCCIÓN (api/routes.py)
# ───────────────────────────────────────────────────────────────
def create_alumno_service():
    """Factory que crea el servicio con sus dependencias reales."""
    repository = SupabaseAlumnoRepository()
    return AlumnoService(repository)

# USO EN TESTS (tests/test_alumno_service.py)
# ───────────────────────────────────────────────────────────────
def test_crear_alumno():
    """Test que usa un repository falso."""
    fake_repository = FakeAlumnoRepository()
    service = AlumnoService(fake_repository)
    
    resultado = service.crear_alumno("Juan", "Pérez", "12345678")
    
    assert resultado.nombre == "Juan"
```

---

#### 🔷 FACTORY METHOD

**Propósito**: Encapsular la lógica de creación de objetos, especialmente cuando hay validación o transformación.

**¿Por qué SÍ?**
- Validación centralizada al crear objetos
- Consistencia: todos los Alumnos se crean igual
- Semántica clara: `Alumno.from_dict(data)` es más legible

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: FACTORY METHOD
# ═══════════════════════════════════════════════════════════════

class Alumno:
    """
    Entidad de dominio que representa un Alumno.
    """
    
    def __init__(self, nombre: str, apellido: str, dni: str, id: str = None):
        # Validaciones en constructor = objetos siempre válidos
        self._validar_nombre(nombre)
        self._validar_apellido(apellido)
        self._validar_dni(dni)
        
        self.id = id
        self.nombre = nombre.strip().title()
        self.apellido = apellido.strip().title()
        self.dni = dni.strip()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Alumno':
        """
        FACTORY METHOD: Crea un Alumno desde un diccionario.
        
        POR QUÉ FACTORY:
        - Centralizo la conversión dict → Alumno
        - Manejo campos opcionales consistentemente
        - Un solo lugar para modificar si cambia la estructura
        
        Uso típico:
            response = supabase.table("alumnos").select("*").execute()
            alumnos = [Alumno.from_dict(row) for row in response.data]
        """
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            dni=data.get('dni', '')
        )
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario para serialización."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni
        }
```

---

#### 🔷 SINGLETON

**Propósito**: Garantizar una única instancia de un recurso compartido (conexión a BD).

**¿Por qué SÍ?**
- Eficiencia: una sola conexión, no una por request
- Consistencia: todos usan el mismo cliente
- Control: un solo punto de configuración

**¿Por qué NO múltiples conexiones?**
- Agota el pool de conexiones
- Inconsistencias de estado
- Overhead innecesario

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: SINGLETON (Thread-Safe)
# ═══════════════════════════════════════════════════════════════

# infrastructure/supabase_client.py
# ───────────────────────────────────────────────────────────────
import os
from supabase import create_client, Client
from threading import Lock

# Variables a nivel de módulo (el "singleton")
_supabase_client: Client = None
_lock = Lock()

def get_supabase_client() -> Client:
    """
    SINGLETON: Retorna siempre la misma instancia del cliente Supabase.
    
    POR QUÉ SINGLETON:
    - Supabase mantiene un pool de conexiones interno
    - Crear múltiples clientes = múltiples pools = desperdicio
    - Thread-safe: el Lock previene race conditions
    
    POR QUÉ NO VARIABLE GLOBAL SIMPLE:
    - Lazy initialization: solo se crea cuando se necesita
    - Seguridad: las credenciales se leen de env, no hardcodeadas
    
    ⚠️ NOTA STATELESS:
    Este singleton es SEGURO en serverless porque:
    - Solo mantiene configuración de conexión
    - No guarda estado de usuario/sesión
    - Cada request usa el cliente, pero no modifica su estado
    """
    global _supabase_client
    
    if _supabase_client is None:
        with _lock:
            # Double-check locking pattern
            if _supabase_client is None:
                url = os.getenv('SUPABASE_URL')
                key = os.getenv('SUPABASE_KEY')
                
                if not url or not key:
                    raise ValueError(
                        "SUPABASE_URL y SUPABASE_KEY deben estar configuradas. "
                        "Nunca hardcodees credenciales en el código."
                    )
                
                _supabase_client = create_client(url, key)
    
    return _supabase_client
```

---

#### 🔷 ADAPTER PATTERN

**Propósito**: Convertir la interface de Supabase a nuestra interface de Repository.

**¿Por qué SÍ?**
- Aíslo los detalles de Supabase en un solo lugar
- Mi código habla "Alumno", no "Supabase Response Data"
- Si Supabase cambia su API, solo modifico el adapter

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: ADAPTER PATTERN
# ═══════════════════════════════════════════════════════════════

# El SupabaseAlumnoRepository ES un Adapter que:
# - Recibe llamadas en términos de dominio (Alumno)
# - Las traduce a llamadas Supabase
# - Retorna objetos de dominio (no responses de Supabase)

class SupabaseAlumnoRepository(AlumnoRepository):
    """
    ADAPTER: Adapta la API de Supabase a nuestra interface de Repository.
    
    Supabase habla en:          Nosotros hablamos en:
    ─────────────────           ────────────────────
    .table("alumnos")           repository.crear(alumno)
    .insert(dict)               Alumno(nombre, apellido, dni)
    .execute()                  
    response.data[0]            → Alumno
    
    El adapter traduce de uno a otro.
    """
    
    def crear(self, alumno: Alumno) -> Alumno:
        # 1. Traduzco Alumno → dict (formato Supabase)
        supabase_data = {
            "nombre": alumno.nombre,
            "apellido": alumno.apellido,
            "dni": alumno.dni
        }
        
        # 2. Llamo a Supabase en su idioma
        response = self._client.table(self._table).insert(supabase_data).execute()
        
        # 3. Traduzco response → Alumno (nuestro idioma)
        return Alumno.from_dict(response.data[0])
```

---

#### 🔷 DECORATOR PATTERN (para Middleware)

**Propósito**: Añadir comportamiento (autenticación) a funciones existentes sin modificarlas.

**¿Por qué SÍ?**
- Separación de concerns: la ruta no sabe de auth
- Reutilizable: un decorador, muchas rutas
- Limpio: `@require_auth` es explícito y declarativo

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: DECORATOR PATTERN (Middleware Auth)
# ═══════════════════════════════════════════════════════════════

# api/middleware/auth.py
# ───────────────────────────────────────────────────────────────
from functools import wraps
from flask import request, jsonify
import jwt
import os

def require_auth(f):
    """
    DECORATOR: Añade validación de JWT a cualquier ruta.
    
    POR QUÉ DECORATOR:
    - La lógica de auth está en UN solo lugar
    - Las rutas quedan limpias y enfocadas en su tarea
    - Fácil de testear: puedo mockear este decorador
    
    Uso:
        @app.route('/api/alumnos', methods=['POST'])
        @require_auth  # <-- Solo agrego esta línea
        def crear_alumno():
            # Esta función solo se ejecuta si el JWT es válido
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token requerido'}), 401
        
        try:
            # Extraer token: "Bearer <token>"
            token = auth_header.split(' ')[1]
            
            # Validar con Supabase JWT secret
            jwt_secret = os.getenv('SUPABASE_JWT_SECRET')
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            
            # Adjuntar usuario al request para uso posterior
            request.user = payload
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Sesión expirada'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


# USO EN RUTAS (api/routes.py)
# ───────────────────────────────────────────────────────────────
@app.route('/api/alumnos', methods=['GET'])
@require_auth
def listar_alumnos():
    # Este código SOLO se ejecuta si el JWT es válido
    service = create_alumno_service()
    alumnos = service.listar_todos()
    return jsonify([a.to_dict() for a in alumnos])
```

---

#### 🔷 STRATEGY PATTERN (Extensibilidad Futura)

**Propósito**: Permitir diferentes algoritmos intercambiables para una misma operación.

**Uso futuro potencial**:
- Diferentes validadores de DNI (Argentina, España, etc.)
- Diferentes formatos de exportación (JSON, CSV, Excel)
- Diferentes proveedores de auth

```python
# ═══════════════════════════════════════════════════════════════
# EJEMPLO: STRATEGY PATTERN (Extensibilidad)
# ═══════════════════════════════════════════════════════════════

# Este patrón NO se implementará ahora, pero la arquitectura lo permite.
# Lo documento para mostrar cómo extender el sistema en el futuro.

from abc import ABC, abstractmethod

class ValidadorDNI(ABC):
    """Strategy interface para validación de DNI."""
    
    @abstractmethod
    def validar(self, dni: str) -> bool:
        pass
    
    @abstractmethod
    def formatear(self, dni: str) -> str:
        pass


class ValidadorDNIArgentina(ValidadorDNI):
    """Implementación para Argentina: 8 dígitos."""
    
    def validar(self, dni: str) -> bool:
        return dni.isdigit() and len(dni) == 8
    
    def formatear(self, dni: str) -> str:
        return f"{dni[:2]}.{dni[2:5]}.{dni[5:]}"


class ValidadorDNIEspana(ValidadorDNI):
    """Implementación para España: 8 dígitos + letra."""
    
    def validar(self, dni: str) -> bool:
        return len(dni) == 9 and dni[:-1].isdigit() and dni[-1].isalpha()
    
    def formatear(self, dni: str) -> str:
        return dni.upper()


# La entidad Alumno podría recibir el validador por inyección:
# alumno = Alumno(nombre, apellido, dni, validador=ValidadorDNIArgentina())
```

---

## 3. Estrategia de Integración (APIs)

### 3.1 API Externa Identificada: Supabase

Aunque Supabase es nuestra única "API externa", aplicamos principios de aislamiento para mantener el código limpio y portable.

```
┌─────────────────────────────────────────────────────────────────┐
│                 ESTRATEGIA DE AISLAMIENTO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   NUESTRO CÓDIGO        │       SUPABASE (Externo)              │
│   ─────────────────     │       ─────────────────               │
│                         │                                       │
│   AlumnoService         │                                       │
│        │                │                                       │
│        ▼                │                                       │
│   AlumnoRepository      │                                       │
│   (Interface)           │                                       │
│        │                │                                       │
│        ▼                │                                       │
│   ┌─────────────────────┼───────────────────────────────────┐  │
│   │  SupabaseAlumno     │  ◄────  FRONTERA DE AISLAMIENTO   │  │
│   │  Repository         │                                   │  │
│   │  (Adapter)          │                                   │  │
│   └─────────────────────┼───────────────────────────────────┘  │
│                         │                                       │
│                         │       supabase-py SDK                 │
│                         │            │                          │
│                         │            ▼                          │
│                         │       Supabase Cloud                  │
│                         │       (PostgreSQL)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Principios de Aislamiento Aplicados

| Principio | Implementación | Beneficio |
|-----------|----------------|-----------|
| **Single Point of Contact** | Solo `supabase_alumno_repository.py` importa `supabase` | Un solo archivo para modificar si cambia la API |
| **Interface Segregation** | Repository interface define solo lo que necesitamos | No dependemos de features de Supabase que no usamos |
| **Error Wrapping** | Capturamos excepciones de Supabase y lanzamos las nuestras | El servicio no ve errores específicos de Supabase |
| **Data Mapping** | `Alumno.from_dict()` y `to_dict()` | Nuestro código habla en entidades, no en dicts de Supabase |

### 3.3 Manejo de Errores de API Externa

```python
# infrastructure/supabase_alumno_repository.py
# ───────────────────────────────────────────────────────────────

from domain.exceptions import RepositoryError, AlumnoNoEncontrado, DNIDuplicado

class SupabaseAlumnoRepository(AlumnoRepository):
    
    def crear(self, alumno: Alumno) -> Alumno:
        try:
            response = self._client.table(self._table).insert({
                "nombre": alumno.nombre,
                "apellido": alumno.apellido,
                "dni": alumno.dni
            }).execute()
            
            return Alumno.from_dict(response.data[0])
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Traducir errores de Supabase a errores de dominio
            if 'unique' in error_msg and 'dni' in error_msg:
                raise DNIDuplicado(f"El DNI {alumno.dni} ya está registrado")
            
            # Error genérico de repository
            raise RepositoryError(f"Error al crear alumno: {e}")
```

---

## 4. Estrategia Stateless

### 4.1 Declaración de Arquitectura Stateless

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     ⚠️  ARQUITECTURA STATELESS OBLIGATORIA  ⚠️                ║
║                                                                              ║
║  Este proyecto está diseñado para funcionar en entornos SERVERLESS          ║
║  (Vercel, Netlify, AWS Lambda) donde:                                        ║
║                                                                              ║
║  • Cada request puede ejecutarse en una instancia DIFERENTE                  ║
║  • La memoria RAM se DESTRUYE después de cada request (o timeout)            ║
║  • NO hay garantía de que dos requests consecutivos compartan estado         ║
║                                                                              ║
║  POR LO TANTO, ESTÁ TERMINANTEMENTE PROHIBIDO:                               ║
║                                                                              ║
║  ❌  Guardar sesiones en variables globales                                   ║
║  ❌  Usar cachés en memoria para datos de usuario                             ║
║  ❌  Mantener contadores o estado mutable a nivel de módulo                   ║
║  ❌  Asumir que la instancia persistirá entre requests                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### 4.2 Dónde SÍ Almacenar Estado

| Tipo de Estado | Dónde Almacenar | Ejemplo |
|----------------|-----------------|---------|
| **Sesión de Usuario** | JWT (cliente) | Token en localStorage → Header Authorization |
| **Datos Persistentes** | Supabase (BD) | Tabla `alumnos` |
| **Preferencias UI** | localStorage (cliente) | Tema oscuro/claro |
| **Datos Temporales** | JWT claims | `user_id`, `email` |

### 4.3 Código Prohibido vs Código Permitido

```python
# ═══════════════════════════════════════════════════════════════
# ❌ CÓDIGO PROHIBIDO (ROMPE EN SERVERLESS)
# ═══════════════════════════════════════════════════════════════

# PROHIBIDO: Variable global mutable para sesiones
usuarios_activos = {}  # ❌ Se pierde entre requests

def login(user_id, token):
    usuarios_activos[user_id] = token  # ❌ Inútil en serverless

def verificar_sesion(user_id):
    return user_id in usuarios_activos  # ❌ Siempre False en nueva instancia


# PROHIBIDO: Caché en memoria
cache_alumnos = []  # ❌ Se pierde

def listar_alumnos():
    global cache_alumnos
    if not cache_alumnos:  # ❌ Siempre vacío en serverless
        cache_alumnos = fetch_from_db()
    return cache_alumnos


# PROHIBIDO: Contador global
request_count = 0  # ❌ Se resetea

def contar_request():
    global request_count
    request_count += 1  # ❌ Siempre será 1


# ═══════════════════════════════════════════════════════════════
# ✅ CÓDIGO PERMITIDO (FUNCIONA EN SERVERLESS)
# ═══════════════════════════════════════════════════════════════

# PERMITIDO: Configuración inmutable a nivel de módulo
TIMEOUT_SEGUNDOS = 30  # ✅ Constante, no cambia
TABLA_ALUMNOS = "alumnos"  # ✅ Constante


# PERMITIDO: Singleton de cliente (no guarda estado de usuario)
_supabase_client = None

def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(url, key)
    return _supabase_client
    # ✅ El cliente es stateless, solo mantiene configuración de conexión


# PERMITIDO: Estado en JWT (viaja con cada request)
def obtener_usuario_actual(request):
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, secret, algorithms=['HS256'])
    return payload['user_id']  # ✅ Estado viene del token, no de RAM


# PERMITIDO: Estado en BD (persistente)
def listar_alumnos():
    # ✅ Consulta la BD en cada request, sin caché
    response = supabase.table("alumnos").select("*").execute()
    return response.data
```

### 4.4 Flujo de Autenticación Stateless

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUJO DE AUTENTICACIÓN STATELESS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. LOGIN (Frontend)                                                        │
│  ────────────────────                                                       │
│     Usuario ingresa email + password                                        │
│           │                                                                 │
│           ▼                                                                 │
│     supabase.auth.signInWithPassword({ email, password })                   │
│           │                                                                 │
│           ▼                                                                 │
│     Supabase valida → Retorna JWT                                           │
│           │                                                                 │
│           ▼                                                                 │
│     Frontend guarda JWT en localStorage                                     │
│                                                                             │
│  2. REQUEST AUTENTICADO (Cada operación)                                    │
│  ────────────────────────────────────────                                   │
│     Frontend lee JWT de localStorage                                        │
│           │                                                                 │
│           ▼                                                                 │
│     fetch('/api/alumnos', {                                                 │
│         headers: {                                                          │
│             'Authorization': `Bearer ${jwt}`  // ← JWT viaja aquí          │
│         }                                                                   │
│     })                                                                      │
│           │                                                                 │
│           ▼                                                                 │
│     Backend recibe request (puede ser instancia nueva)                      │
│           │                                                                 │
│           ▼                                                                 │
│     Middleware extrae JWT del header                                        │
│           │                                                                 │
│           ▼                                                                 │
│     Middleware valida firma del JWT                                         │
│           │                                                                 │
│           ├─── Válido ───► Continúa al handler                             │
│           │                                                                 │
│           └─── Inválido ──► 401 Unauthorized                               │
│                                                                             │
│  3. EL ESTADO NUNCA ESTÁ EN EL SERVIDOR                                    │
│  ────────────────────────────────────────                                   │
│     • JWT contiene: user_id, email, exp (expiración)                       │
│     • Servidor NO guarda "quién está logueado"                             │
│     • Cada request es auto-contenido                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Watchdog de Inactividad (Frontend)

```javascript
// static/js/app.js
// ═══════════════════════════════════════════════════════════════

/**
 * WATCHDOG DE INACTIVIDAD
 * 
 * POR QUÉ EN FRONTEND:
 * - El backend es stateless, no puede "recordar" cuándo fue el último request
 * - El frontend SÍ puede trackear actividad del usuario
 * - Cumple con RNF-003: timeout de 15 minutos
 * 
 * IMPLEMENTACIÓN:
 * - Timer que se resetea con cualquier actividad
 * - Si expira → cierre de sesión automático
 */

const INACTIVITY_TIMEOUT_MS = 15 * 60 * 1000; // 15 minutos
let inactivityTimer = null;

function initInactivityWatchdog() {
    // Eventos que consideramos "actividad"
    const activityEvents = ['click', 'keypress', 'scroll', 'mousemove', 'touchstart'];
    
    activityEvents.forEach(eventType => {
        document.addEventListener(eventType, resetInactivityTimer, { passive: true });
    });
    
    // Iniciar el timer
    resetInactivityTimer();
}

function resetInactivityTimer() {
    // Limpiar timer anterior
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
    }
    
    // Crear nuevo timer
    inactivityTimer = setTimeout(() => {
        // Timeout alcanzado → cerrar sesión
        console.warn('Sesión cerrada por inactividad (15 minutos)');
        cerrarSesion(true); // true = mostrar mensaje
    }, INACTIVITY_TIMEOUT_MS);
}

async function cerrarSesion(porInactividad = false) {
    try {
        await supabase.auth.signOut();
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    }
    
    // Limpiar timer
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
        inactivityTimer = null;
    }
    
    // Mostrar mensaje si fue por inactividad
    if (porInactividad) {
        alert('Tu sesión ha sido cerrada por inactividad. Por favor, inicia sesión nuevamente.');
    }
    
    // Redirigir a login
    window.location.reload();
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initInactivityWatchdog);
```

### 4.6 Checklist de Validación Stateless

Antes de cada deploy, verificar:

| # | Verificación | Comando/Método | ✅/❌ |
|---|--------------|----------------|-------|
| 1 | No hay `global` + asignación (excepto singleton de cliente) | `grep -r "global " --include="*.py"` | ⬜ |
| 2 | No hay diccionarios mutables a nivel de módulo | Revisión manual | ⬜ |
| 3 | No hay `session = {}` o similar | `grep -r "session\s*=" --include="*.py"` | ⬜ |
| 4 | JWT se valida en cada request | Revisar middleware | ⬜ |
| 5 | Funciona en local igual que en Vercel | Test manual | ⬜ |

---

## 5. Estructura de Carpetas Detallada

```
app-prueba-didactica/
│
├── 📁 api/                              # CAPA DE PRESENTACIÓN
│   │
│   │   # POR QUÉ ESTA CAPA:
│   │   # - Punto de entrada HTTP
│   │   # - Traduce HTTP ↔ Casos de uso
│   │   # - NO contiene lógica de negocio
│   │
│   ├── __init__.py
│   ├── routes.py                        # Definición de rutas Flask
│   ├── index.py                         # Handler para Vercel (entry point)
│   └── middleware/
│       ├── __init__.py
│       └── auth.py                      # Decorador @require_auth
│
├── 📁 application/                      # CAPA DE APLICACIÓN
│   │
│   │   # POR QUÉ ESTA CAPA:
│   │   # - Orquesta casos de uso
│   │   # - Coordina entre dominio e infraestructura
│   │   # - Contiene lógica de aplicación (no de negocio)
│   │
│   ├── __init__.py
│   └── alumno_service.py                # Casos de uso de Alumno
│
├── 📁 domain/                           # CAPA DE DOMINIO (EL CORAZÓN)
│   │
│   │   # POR QUÉ ESTA CAPA:
│   │   # - Entidades y reglas de negocio PURAS
│   │   # - SIN dependencias externas (no Flask, no Supabase)
│   │   # - Testeable sin infraestructura
│   │
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── alumno.py                    # Entidad Alumno con validaciones
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── alumno_repository.py         # Interface abstracta (ABC)
│   └── exceptions.py                    # Excepciones de dominio
│
├── 📁 infrastructure/                   # CAPA DE INFRAESTRUCTURA
│   │
│   │   # POR QUÉ ESTA CAPA:
│   │   # - Implementaciones concretas
│   │   # - Conoce detalles técnicos (Supabase, APIs)
│   │   # - Implementa interfaces del dominio
│   │
│   ├── __init__.py
│   ├── supabase_client.py               # Singleton del cliente Supabase
│   └── supabase_alumno_repository.py    # Implementación del repository
│
├── 📁 static/                           # FRONTEND
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js                       # Lógica + Supabase SDK
│   └── index.html
│
├── 📁 tests/                            # TESTING ATÓMICO
│   ├── __init__.py
│   ├── test_alumno.py                   # Tests de entidad
│   ├── test_alumno_repository.py        # Tests con mock
│   ├── test_alumno_service.py           # Tests de servicio
│   └── test_api.py                      # Tests de integración
│
├── 📁 docs/                             # DOCUMENTACIÓN
│   ├── 01_planificacion_analisis.md
│   ├── 02_a_arquitectura_patrones.md    # ← Este archivo
│   ├── CHECKPOINT.md
│   └── MANUAL_TECNICO.md                # (Futuro)
│
├── 📄 .env.example                      # Template de variables
├── 📄 .gitignore
├── 📄 requirements.txt
├── 📄 vercel.json                       # (Futuro)
├── 📄 Dockerfile                        # (Futuro)
├── 📄 run_local.py                      # Entry point local
└── 📄 README.md
```

---

## 📊 Resumen de Decisiones Arquitectónicas

| Decisión | Opción Elegida | Justificación |
|----------|----------------|---------------|
| Arquitectura | Clean Architecture | Separación de responsabilidades, testeable, didáctico |
| Patrón de Datos | Repository Pattern | Abstrae BD, permite mocks, desacoplado |
| Dependencias | Inyección de Dependencias | Testeable, flexible, explícito |
| Creación de Objetos | Factory Method | Validación centralizada, consistencia |
| Conexión BD | Singleton | Eficiencia, una conexión compartida |
| APIs Externas | Adapter Pattern | Aísla dependencias, traducción de interfaces |
| Autenticación | Decorator Pattern | Limpio, reutilizable, declarativo |
| Estado | Stateless (JWT + BD) | Compatible con serverless |
| Inactividad | Watchdog Frontend | 15 min timeout, cumple RNF-003 |

---

> **Estado del Documento**: Pendiente de Aprobación  
> **Siguiente Paso**: Implementación de Capa de Dominio (Phase 3-B)
