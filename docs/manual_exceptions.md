# Manual Tecnico: domain/exceptions.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Domain (Capa de Dominio)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo define las **excepciones personalizadas del dominio**. Son clases que representan errores de negocio y permiten un manejo de errores semantico y estructurado.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Domain Layer |
| **Historias de Usuario** | HU-001, HU-003, HU-004 |
| **Criterios de Aceptacion** | CA-001.2 (DNI unico), CA-004.1 (Confirmacion) |
| **Requisitos Funcionales** | RF-005 (Validacion), RF-009 (Confirmacion) |
| **Patron** | Domain Exception Pattern |

### 1.3 Por Que Excepciones Personalizadas

**SI se eligio**:
- Excepciones con significado de negocio (no genericas)
- Incluyen codigo, mensaje y campo afectado
- Facilitan respuestas HTTP semanticas (400, 404, 409)
- Metodo `to_dict()` para serializacion JSON

**NO se eligio**:
- Excepciones genericas de Python (`Exception`, `ValueError`)
- Codigos de error numericos sin contexto
- Logs sin estructura

---

## 2. Estrategia de Construccion

### 2.1 Jerarquia de Excepciones

```
DomainException (base)
|-- ValidacionError (datos invalidos)
|-- AlumnoNoEncontrado (404)
|-- DNIDuplicado (409 conflict)
|-- RepositoryError (error de BD)
|-- AuthenticationError (401)
    |-- SessionExpiredError (sesion expirada)
```

### 2.2 Estructura Comun

Cada excepcion incluye:
- `message`: Descripcion legible
- `codigo`: Codigo unico para el frontend
- `campo`: Campo afectado (opcional)
- `to_dict()`: Serializacion a JSON

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Verifica que todas las excepciones se pueden instanciar
2. Valida el metodo `to_dict()`
3. Prueba la jerarquia de herencia

**Por que es obligatorio**:
- Permite ejecutar `python domain/exceptions.py` directamente
- Valida el archivo de forma aislada
- Documenta el comportamiento esperado

---

## 4. Codigo Fuente

### 4.1 Clase Base

```python
class DomainException(Exception):
    def __init__(self, message: str, codigo: str = "DOMAIN_ERROR"):
        self.message = message
        self.codigo = codigo
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        return {
            'error': self.message,
            'codigo': self.codigo
        }
```

### 4.2 Excepciones Especificas

| Excepcion | Codigo | Uso |
|-----------|--------|-----|
| `ValidacionError` | VALIDATION_ERROR | Datos invalidos |
| `AlumnoNoEncontrado` | ALUMNO_NOT_FOUND | ID no existe |
| `DNIDuplicado` | DNI_DUPLICADO | DNI ya registrado |
| `RepositoryError` | REPOSITORY_ERROR | Error de BD |
| `AuthenticationError` | AUTH_ERROR | Sin autenticacion |
| `SessionExpiredError` | SESSION_EXPIRED | Sesion expirada |

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python domain/exceptions.py
```

### 5.2 Salida Esperada

```
=== Prueba de Excepciones de Dominio ===

[OK] DomainException creada correctamente
[OK] ValidacionError creada correctamente
[OK] AlumnoNoEncontrado creada correctamente
[OK] DNIDuplicado creada correctamente
[OK] RepositoryError creada correctamente
[OK] AuthenticationError creada correctamente
[OK] SessionExpiredError creada correctamente

=== Todas las pruebas pasaron ===
```

### 5.3 Unit Test Rapido

```python
def test_validacion_error_tiene_campo():
    error = ValidacionError("Error", "nombre")
    assert error.campo == "nombre"
    assert error.codigo == "VALIDATION_ERROR"
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Clase base abstracta | Permite `except DomainException` para atrapar todas |
| Codigo unico | Frontend puede traducir mensajes |
| Campo afectado | Permite resaltar input con error |
| `to_dict()` | Serializacion directa a JSON |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| `raise Exception("error")` | Sin contexto, dificil de manejar |
| Codigos numericos (1001, 1002) | No autoexplicativos |
| Retornar None en vez de excepcion | Oculta errores, dificil debug |
| Imprimir errores a consola | No permite manejo programatico |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `ImportError: DomainException` | Path incorrecto | Ejecutar desde raiz del proyecto |
| `AttributeError: 'NoneType'` | Campo no pasado | Verificar constructor |
| Test falla | Cambio en estructura | Actualizar prueba atomica |

### 7.2 Uso Correcto en Codigo

```python
# En servicio
from domain.exceptions import ValidacionError

def crear_alumno(nombre):
    if not nombre:
        raise ValidacionError("Nombre es requerido", "nombre")

# En API
try:
    servicio.crear_alumno("")
except ValidacionError as e:
    return jsonify(e.to_dict()), 400
```

---

> **Manual Tecnico**: domain/exceptions.py  
> **Version**: 1.0.0
