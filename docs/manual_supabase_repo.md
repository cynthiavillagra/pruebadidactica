# Manual Tecnico: infrastructure/supabase_alumno_repository.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Infrastructure (Capa de Infraestructura)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo implementa el **repositorio de Supabase** para la entidad Alumno. Es la implementacion concreta de la interface `AlumnoRepository` que traduce las operaciones CRUD a llamadas a la API de Supabase.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Infrastructure Layer |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004 |
| **Requisitos Funcionales** | RF-001, RF-002, RF-003, RF-004 |
| **Patron** | Repository (Implementation), Adapter |

### 1.3 Por Que Adapter Pattern

**SI se eligio**:
- Traduce entre dominio y Supabase
- Mapea dict a entidad y viceversa
- Encierra logica especifica de Supabase
- Permite cambiar BD sin tocar dominio

**NO se eligio**:
- Usar Supabase directamente en servicios
- Exponer tipos de Supabase al dominio
- Logica de BD en multiples archivos

---

## 2. Estrategia de Construccion

### 2.1 Implementacion del Contrato

| Metodo | Operacion Supabase | Equivalente SQL |
|--------|-------------------|-----------------|
| `crear` | `table.insert()` | INSERT |
| `obtener_por_id` | `table.select().eq('id')` | SELECT WHERE id = |
| `obtener_por_dni` | `table.select().eq('dni')` | SELECT WHERE dni = |
| `listar_todos` | `table.select().order()` | SELECT ORDER BY |
| `actualizar` | `table.update().eq('id')` | UPDATE WHERE id = |
| `eliminar` | `table.delete().eq('id')` | DELETE WHERE id = |
| `existe_dni` | `table.select('id').eq('dni')` | EXISTS |

### 2.2 Mapeo de Datos

```python
def _map_to_entity(self, data: dict) -> Alumno:
    """Convierte respuesta de Supabase a entidad de dominio."""
    return Alumno.from_dict(data)
```

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Crea el repositorio
2. Intenta listar alumnos (verifica conexion)
3. Muestra los primeros 3 alumnos

**Requiere**: `.env` configurado con credenciales validas.

### 3.2 Manejo de Errores

```python
try:
    response = self.table.insert(data).execute()
except Exception as e:
    if 'duplicate key' in str(e).lower():
        raise DNIDuplicado(alumno.dni)
    raise RepositoryError(f"Error: {e}")
```

---

## 4. Codigo Fuente

### 4.1 Lazy Client Loading

```python
@property
def client(self):
    """Obtiene el cliente Supabase (lazy loading)."""
    if self._client is None:
        self._client = get_supabase_client()
    return self._client

@property
def table(self):
    """Acceso directo a la tabla de alumnos."""
    return self.client.table(self.TABLE_NAME)
```

### 4.2 Metodo Crear

```python
def crear(self, alumno: Alumno) -> Alumno:
    # Verificar DNI unico antes de insertar
    if self.existe_dni(alumno.dni):
        raise DNIDuplicado(alumno.dni)
    
    data = {
        'nombre': alumno.nombre,
        'apellido': alumno.apellido,
        'dni': alumno.dni
    }
    
    response = self.table.insert(data).execute()
    return self._map_to_entity(response.data[0])
```

### 4.3 Metodo Existe DNI

```python
def existe_dni(self, dni: str, excluir_id: Optional[str] = None) -> bool:
    query = self.table.select('id').eq('dni', dni.upper())
    
    if excluir_id:
        query = query.neq('id', excluir_id)
    
    response = query.execute()
    return len(response.data) > 0
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python infrastructure/supabase_alumno_repository.py
```

### 5.2 Salida Esperada (con .env y tabla creada)

```
=== Prueba de SupabaseAlumnoRepository ===

[OK] Repositorio creado
[OK] Listar alumnos: 5 encontrados
     - Garcia, Maria (DNI: 12345678)
     - Lopez, Carlos (DNI: 87654321)
     - Perez, Juan (DNI: 11111111)

=== Prueba pasada ===
```

### 5.3 Salida Esperada (sin configuracion)

```
=== Prueba de SupabaseAlumnoRepository ===

[ADVERTENCIA] Variable de entorno 'SUPABASE_URL' no configurada

Esto es esperado si no tienes .env configurado.
```

### 5.4 Unit Test Rapido

```python
# Este test requiere conexion real, usar para integracion
def test_listar_no_falla():
    repo = SupabaseAlumnoRepository()
    alumnos = repo.listar_todos()
    assert isinstance(alumnos, list)
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Lazy client loading | Solo conecta cuando se usa |
| Verificar DNI antes de insert | Evita error de BD |
| `_map_to_entity` | Centraliza conversion |
| Ordenar por apellido | UX consistente |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| ORM (SQLAlchemy) | Overkill para esta app |
| Queries SQL raw | Menos seguro, mas complejo |
| Sin validacion de DNI | Error de BD menos claro |
| Retornar dicts | Perdemos validaciones de entidad |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `DNIDuplicado` | DNI ya existe | Usar otro DNI |
| `relation 'alumnos' does not exist` | Tabla no creada | Ejecutar init.sql |
| `row-level security` | RLS sin politicas | Agregar politicas o desactivar |
| `Invalid API key` | Key incorrecta | Verificar SUPABASE_KEY |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel |
|---------|-------|--------|
| Conexion | Directa a Supabase | Igual |
| Latencia | ~50-100ms | Variable |
| Timeout | Sin limite | 10s (serverless) |

---

> **Manual Tecnico**: infrastructure/supabase_alumno_repository.py  
> **Version**: 1.0.0
