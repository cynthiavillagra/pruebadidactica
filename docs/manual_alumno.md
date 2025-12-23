# Manual Tecnico: domain/entities/alumno.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Domain (Capa de Dominio - Entidades)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo define la **entidad Alumno**, el objeto central del dominio. Contiene las reglas de negocio y validaciones que definen que es un alumno valido.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Domain Layer - Entities |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004 |
| **Criterios de Aceptacion** | CA-001.1 (Campos obligatorios), CA-001.2 (DNI unico) |
| **Requisitos Funcionales** | RF-001, RF-002, RF-003, RF-004, RF-005 |
| **Patron** | Entity, Value Object, Factory Method |

### 1.3 Por Que Entidad Rica

**SI se eligio**:
- Validacion en el constructor (nunca existe en estado invalido)
- Propiedades inmutables (solo getters, no setters)
- Factory methods (`from_dict`, `to_dict`)
- Metodos de dominio (`actualizar`, `es_nuevo`)

**NO se eligio**:
- Modelo anemico (solo datos sin logica)
- Validacion externa (en servicio)
- Mutabilidad directa de atributos

---

## 2. Estrategia de Construccion

### 2.1 Atributos de la Entidad

| Atributo | Tipo | Validacion | Fuente |
|----------|------|------------|--------|
| `id` | str (UUID) | Generado automaticamente | Supabase |
| `nombre` | str | Requerido, max 100 chars | Usuario |
| `apellido` | str | Requerido, max 100 chars | Usuario |
| `dni` | str | Requerido, unico | Usuario |
| `created_at` | datetime | UTC automatico | Sistema |
| `updated_at` | datetime | UTC automatico | Sistema |

### 2.2 Normalizaciones Automaticas

| Campo | Normalizacion |
|-------|---------------|
| nombre | `strip().title()` |
| apellido | `strip().title()` |
| dni | `strip().upper()` |

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Crea un alumno valido
2. Prueba validaciones (nombre vacio, DNI vacio)
3. Verifica `from_dict` y `to_dict`
4. Prueba el metodo `actualizar`

### 3.2 Por Que Inmutabilidad

```python
# MAL: Mutacion directa
alumno.nombre = "Nuevo Nombre"  # NO permitido

# BIEN: Crear nueva instancia
alumno_nuevo = alumno.actualizar(nombre="Nuevo Nombre")
```

**Beneficios**:
- Previene efectos secundarios
- Facilita testing
- Claridad en el codigo

---

## 4. Codigo Fuente

### 4.1 Constructor con Validacion

```python
def __init__(self, nombre: str, apellido: str, dni: str, ...):
    # Validar ANTES de asignar
    self._validar_campo(nombre, "nombre")
    self._validar_campo(apellido, "apellido")
    self._validar_campo(dni, "dni")
    
    # Normalizar y asignar
    self._nombre = nombre.strip().title()
    self._apellido = apellido.strip().title()
    self._dni = dni.strip().upper()
```

### 4.2 Factory Method

```python
@classmethod
def from_dict(cls, data: dict) -> 'Alumno':
    """Crea Alumno desde diccionario (ej: respuesta de Supabase)."""
    return cls(
        id=data.get('id'),
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        dni=data.get('dni'),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )
```

### 4.3 Metodo de Dominio

```python
def actualizar(self, **kwargs) -> 'Alumno':
    """Crea NUEVA instancia con datos actualizados."""
    return Alumno(
        id=self._id,
        nombre=kwargs.get('nombre', self._nombre),
        apellido=kwargs.get('apellido', self._apellido),
        dni=kwargs.get('dni', self._dni),
        created_at=self._created_at
    )
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python domain/entities/alumno.py
```

### 5.2 Salida Esperada

```
=== Prueba de Entidad Alumno ===

[OK] Crear alumno valido: Juan Perez (DNI: 12345678)
[OK] Nombre normalizado a Title Case
[OK] DNI normalizado a mayusculas
[OK] Nombre vacio lanza ValidacionError
[OK] DNI vacio lanza ValidacionError
[OK] from_dict funciona correctamente
[OK] to_dict funciona correctamente
[OK] actualizar crea nueva instancia

=== Todas las pruebas pasaron ===
```

### 5.3 Unit Test Rapido

```python
def test_alumno_valido():
    alumno = Alumno(nombre="juan", apellido="perez", dni="123")
    assert alumno.nombre == "Juan"  # Title case
    assert alumno.dni == "123"
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Validacion en constructor | Imposible tener alumno invalido |
| Properties solo lectura | Inmutabilidad garantizada |
| `from_dict`/`to_dict` | Facilita serializacion |
| Fechas UTC | Estandar global, sin ambiguedad |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Diccionario plano | Sin validacion, sin metodos |
| dataclass sin validacion | Permite estados invalidos |
| Setters publicos | Permite mutacion no controlada |
| Validacion en servicio | Duplicacion de logica |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValidacionError: nombre` | Nombre vacio o solo espacios | Verificar input |
| `AttributeError: _nombre` | Acceso directo a atributo privado | Usar property `alumno.nombre` |
| Fecha incorrecta | Zona horaria local | Siempre usar `timezone.utc` |

### 7.2 Ejemplo de Uso

```python
from domain.entities.alumno import Alumno

# Crear nuevo
alumno = Alumno(nombre="Maria", apellido="Garcia", dni="87654321")

# Desde BD
data = supabase.table('alumnos').select('*').execute()
alumno = Alumno.from_dict(data.data[0])

# Actualizar
actualizado = alumno.actualizar(nombre="Maria Jose")
```

---

> **Manual Tecnico**: domain/entities/alumno.py  
> **Version**: 1.0.0
