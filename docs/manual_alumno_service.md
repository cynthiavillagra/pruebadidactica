# Manual Tecnico: application/alumno_service.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Application (Capa de Aplicacion)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo implementa el **servicio de aplicacion** para Alumnos. Orquesta los casos de uso CRUD coordinando entre la capa de dominio y el repositorio. NO contiene logica de negocio (esa esta en las entidades).

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Application Layer (Service Layer) |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004 |
| **Requisitos Funcionales** | RF-001, RF-002, RF-003, RF-004 |
| **Patron** | Service Layer, Dependency Injection |

### 1.3 Por Que Service Layer

**SI se eligio**:
- Orquesta flujos de negocio
- Recibe repositorio por constructor (DI)
- Coordina sin conocer detalles de BD
- Facil de testear con mock

**NO se eligio**:
- Logica en controladores/routes
- Acceso directo a BD
- Servicios estaticos sin inyeccion

---

## 2. Estrategia de Construccion

### 2.1 Casos de Uso

| Metodo | HU | RF | Descripcion |
|--------|-----|-----|-------------|
| `crear_alumno()` | HU-001 | RF-001 | Crear nuevo alumno |
| `obtener_alumno()` | HU-002 | RF-002 | Obtener por ID |
| `listar_alumnos()` | HU-002 | RF-002 | Listar todos |
| `actualizar_alumno()` | HU-003 | RF-003 | Actualizar existente |
| `eliminar_alumno()` | HU-004 | RF-004 | Eliminar por ID |
| `buscar_por_dni()` | - | - | Busqueda auxiliar |

### 2.2 Dependency Injection

```python
class AlumnoService:
    def __init__(self, repository: AlumnoRepository):
        self._repository = repository
```

**Beneficios**:
- Puede recibir `MockAlumnoRepository` para tests
- Puede recibir `SupabaseAlumnoRepository` para produccion
- Desacoplado de implementacion concreta

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Crea servicio con `MockAlumnoRepository`
2. Ejecuta todos los casos de uso
3. Verifica excepciones (DNI duplicado, no encontrado)

### 3.2 Factory Function

```python
def create_alumno_service() -> AlumnoService:
    """Crea servicio con repositorio de produccion."""
    from infrastructure.supabase_alumno_repository import SupabaseAlumnoRepository
    repository = SupabaseAlumnoRepository()
    return AlumnoService(repository)
```

**Por que factory**:
- Centraliza creacion con dependencias
- Usado por la capa de API
- Facilita cambiar repositorio

---

## 4. Codigo Fuente

### 4.1 Caso de Uso: Crear Alumno

```python
def crear_alumno(self, nombre: str, apellido: str, dni: str) -> Alumno:
    """
    Caso de uso: Crear un nuevo alumno.
    
    Trazabilidad: HU-001, RF-001, RF-005
    """
    # Crear entidad (valida internamente)
    alumno = Alumno(nombre=nombre, apellido=apellido, dni=dni)
    
    # Persistir (el repositorio verifica DNI unico)
    return self._repository.crear(alumno)
```

### 4.2 Caso de Uso: Actualizar Alumno

```python
def actualizar_alumno(self, id: str, nombre: str, apellido: str, dni: str) -> Alumno:
    # Verificar que existe
    alumno_actual = self._repository.obtener_por_id(id)
    if alumno_actual is None:
        raise AlumnoNoEncontrado(id)
    
    # Crear nueva instancia con datos actualizados
    alumno_nuevo = Alumno(
        id=id,
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        created_at=alumno_actual.created_at
    )
    
    return self._repository.actualizar(alumno_nuevo)
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python application/alumno_service.py
```

### 5.2 Salida Esperada

```
=== Prueba de AlumnoService (con Mock) ===

[OK] Crear: Juan Perez (DNI: 11111111)
[OK] Listar: 1 alumnos
[OK] Obtener: Juan Perez (DNI: 11111111)
[OK] Actualizar: Juan Carlos Perez (DNI: 11111111)
[OK] DNI duplicado: El DNI '11111111' ya esta registrado
[OK] Eliminar: True
[OK] No encontrado: Alumno con ID 'mock-id-1' no encontrado

=== Todas las pruebas pasaron ===
```

### 5.3 Unit Test Rapido

```python
def test_crear_alumno_retorna_con_id():
    repo = MockAlumnoRepository()
    service = AlumnoService(repo)
    
    alumno = service.crear_alumno("Juan", "Perez", "12345678")
    
    assert alumno.id is not None
    assert alumno.nombre == "Juan"
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| DI por constructor | Facilita testing y flexibilidad |
| No contiene validacion | Esa logica esta en Alumno |
| Factory function | Centraliza creacion para API |
| Metodos simples | Solo orquestan, no deciden |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Servicio estatico | No permite inyectar mock |
| Validar aqui | Duplica logica de entidad |
| Crear repo internamente | Acoplamiento fuerte |
| Servicios multiples | Un solo servicio es suficiente |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `AlumnoNoEncontrado` | ID no existe | Verificar ID correcto |
| `DNIDuplicado` | DNI ya registrado | Usar otro DNI |
| `ValidacionError` | Datos invalidos | Verificar nombre/apellido/dni |

### 7.2 Uso en API

```python
from application.alumno_service import create_alumno_service

@app.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    service = create_alumno_service()
    data = request.get_json()
    
    try:
        alumno = service.crear_alumno(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni']
        )
        return jsonify(alumno.to_dict()), 201
    except ValidacionError as e:
        return jsonify(e.to_dict()), 400
```

---

> **Manual Tecnico**: application/alumno_service.py  
> **Version**: 1.0.0
