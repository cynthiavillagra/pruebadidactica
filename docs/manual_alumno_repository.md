# Manual Tecnico: domain/repositories/alumno_repository.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Domain (Capa de Dominio - Repositorios)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo define la **interface abstracta del repositorio** de alumnos. Es un contrato que especifica las operaciones CRUD que cualquier implementacion debe cumplir, independientemente de la base de datos usada.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Domain Layer - Repositories |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004 |
| **Requisitos Funcionales** | RF-001, RF-002, RF-003, RF-004 |
| **Patron** | Repository Pattern, Dependency Inversion |

### 1.3 Por Que Interface Abstracta

**SI se eligio**:
- ABC (Abstract Base Class) de Python
- Metodos abstractos sin implementacion
- Desacopla dominio de infraestructura
- Permite cambiar BD sin tocar la logica

**NO se eligio**:
- Acceso directo a BD en servicios
- Repositorio concreto en dominio
- Sin abstraccion (todo acoplado)

---

## 2. Estrategia de Construccion

### 2.1 Contrato del Repositorio

| Metodo | Firma | Retorno | Proposito |
|--------|-------|---------|-----------|
| `crear` | `(alumno: Alumno)` | `Alumno` | RF-001 |
| `obtener_por_id` | `(id: str)` | `Optional[Alumno]` | RF-002 |
| `obtener_por_dni` | `(dni: str)` | `Optional[Alumno]` | Busqueda |
| `listar_todos` | `()` | `List[Alumno]` | RF-002 |
| `actualizar` | `(alumno: Alumno)` | `Alumno` | RF-003 |
| `eliminar` | `(id: str)` | `bool` | RF-004 |
| `existe_dni` | `(dni: str, excluir_id?)` | `bool` | Validacion |

### 2.2 Implementaciones

| Clase | Uso | Ubicacion |
|-------|-----|-----------|
| `AlumnoRepository` | Interface abstracta | Este archivo |
| `MockAlumnoRepository` | Testing | Este archivo |
| `SupabaseAlumnoRepository` | Produccion | infrastructure/ |

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** usando `MockAlumnoRepository`:
1. Crea un alumno
2. Lo busca por ID
3. Lo actualiza
4. Lo elimina
5. Verifica que ya no existe

### 3.2 Por Que Mock en el Mismo Archivo

```python
class MockAlumnoRepository(AlumnoRepository):
    """Implementacion en memoria para testing."""
```

**Beneficios**:
- Pruebas sin BD real
- Rapido de ejecutar
- Documenta el comportamiento esperado
- Usado por tests unitarios

---

## 4. Codigo Fuente

### 4.1 Interface Abstracta

```python
from abc import ABC, abstractmethod

class AlumnoRepository(ABC):
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """Persiste un nuevo alumno."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Alumno]:
        """Busca alumno por ID, retorna None si no existe."""
        pass
    
    # ... otros metodos
```

### 4.2 Mock Implementation

```python
class MockAlumnoRepository(AlumnoRepository):
    def __init__(self):
        self._storage: Dict[str, Alumno] = {}
        self._counter = 0
    
    def crear(self, alumno: Alumno) -> Alumno:
        self._counter += 1
        alumno_con_id = Alumno(
            id=f"mock-id-{self._counter}",
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni
        )
        self._storage[alumno_con_id.id] = alumno_con_id
        return alumno_con_id
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python domain/repositories/alumno_repository.py
```

### 5.2 Salida Esperada

```
=== Prueba de AlumnoRepository (Mock) ===

[OK] Crear alumno: Juan Perez (mock-id-1)
[OK] Obtener por ID: Juan Perez
[OK] Listar todos: 1 alumnos
[OK] Actualizar: Juan Carlos Perez
[OK] Existe DNI: True
[OK] Eliminar: True
[OK] Obtener eliminado: None

=== Todas las pruebas pasaron ===
```

### 5.3 Unit Test Rapido

```python
def test_mock_repository_crud():
    repo = MockAlumnoRepository()
    alumno = Alumno(nombre="Test", apellido="Test", dni="123")
    
    creado = repo.crear(alumno)
    assert creado.id is not None
    
    obtenido = repo.obtener_por_id(creado.id)
    assert obtenido.nombre == "Test"
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| ABC para interface | Fuerza implementacion de metodos |
| `Optional` en retornos | Explicito cuando puede no existir |
| Mock incluido | Pruebas sin dependencias externas |
| Metodo `existe_dni` | Reutilizable para validacion |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Protocolo (Protocol) | Menos explicito que ABC |
| Duck typing | Sin garantia de metodos |
| BD directa en servicio | Violaria Clean Architecture |
| Mock en archivo separado | Rompe cohesion del contrato |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `TypeError: Can't instantiate ABC` | Falta implementar metodo | Agregar todos los `@abstractmethod` |
| `KeyError` en mock | ID no existe | Verificar flujo de creacion |
| Lista desordenada | Sin ordenar en listar | Agregar `sorted()` por apellido |

### 7.2 Como Implementar Nueva BD

```python
# Para implementar con otra BD (ej: MongoDB):
class MongoAlumnoRepository(AlumnoRepository):
    def __init__(self, db):
        self._collection = db['alumnos']
    
    def crear(self, alumno: Alumno) -> Alumno:
        result = self._collection.insert_one(alumno.to_dict())
        # ...
```

---

> **Manual Tecnico**: domain/repositories/alumno_repository.py  
> **Version**: 1.0.0
