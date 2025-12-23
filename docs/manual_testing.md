# Manual de Ejecucion y Validacion Final

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Fase**: 5 - Testing Formal  
> **Fecha**: 2025-12-22

---

## Parte A: Tests Automaticos

### A.1 Requisitos Previos

```powershell
# Asegurar entorno virtual activado
.\venv\Scripts\Activate

# Verificar pytest instalado
pip show pytest
```

### A.2 Ejecutar Todos los Tests

```powershell
# Desde la raiz del proyecto
python -m pytest tests/ -v
```

### A.3 Ejecutar Tests por Archivo

```powershell
# Solo tests de la entidad Alumno
python -m pytest tests/test_alumno.py -v

# Solo tests del servicio
python -m pytest tests/test_alumno_service.py -v

# Solo tests de la API
python -m pytest tests/test_routes.py -v
```

### A.4 Ejecutar con Cobertura

```powershell
# Generar reporte de cobertura
python -m pytest tests/ --cov=domain --cov=application --cov=api --cov-report=term-missing
```

### A.5 Interpretacion de Resultados

| Simbolo | Significado |
|---------|-------------|
| `.` | Test paso |
| `F` | Test fallo |
| `E` | Error en el test |
| `s` | Test saltado |

**Salida esperada**:
```
========================= test session starts ==========================
collected XX items

tests/test_alumno.py ............                               [ 33%]
tests/test_alumno_service.py ............                       [ 67%]
tests/test_routes.py ............                               [100%]

========================= XX passed in X.XXs ===========================
```

### A.6 Solucion de Problemas

| Error | Causa | Solucion |
|-------|-------|----------|
| `ModuleNotFoundError` | Path incorrecto | Ejecutar desde raiz del proyecto |
| `ImportError: pytest` | pytest no instalado | `pip install pytest` |
| `No tests collected` | Nombre incorrecto | Archivos deben empezar con `test_` |

---

## Parte B: Validacion Manual Humana (UAT)

### B.1 Preparacion del Entorno

```powershell
# 1. Asegurar que .env tiene credenciales correctas

# 2. Iniciar servidor
python api/index.py

# 3. Abrir navegador
start http://localhost:5000
```

### B.2 Prerequisitos de Supabase

Antes de ejecutar UAT:

1. **Crear usuario en Supabase**:
   - Ir a Supabase Dashboard > Authentication > Users
   - Click "Add User" > "Create New User"
   - Ingresar email y password

2. **Verificar tabla existe**:
   - Ir a SQL Editor
   - Ejecutar: `SELECT * FROM alumnos LIMIT 1;`

### B.3 Ejecutar Flujos UAT

#### Flujo UAT-01: Registro de Nuevo Alumno

| Paso | Accion | Verificar |
|------|--------|-----------|
| 1 | Iniciar sesion con usuario Supabase | Se muestra pantalla principal |
| 2 | Click "Nuevo Alumno" | Formulario visible |
| 3 | Ingresar: Maria, Garcia, 33445566 | Campos completos |
| 4 | Click "Guardar" | Toast "Alumno creado" |
| 5 | Verificar tabla | Alumno aparece en lista |

**Resultado**: [ ] PASO / [ ] FALLO

#### Flujo UAT-02: Edicion de Alumno

| Paso | Accion | Verificar |
|------|--------|-----------|
| 1 | Click "Editar" en un alumno | Formulario con datos |
| 2 | Cambiar nombre a "Maria Jose" | Campo actualizado |
| 3 | Click "Guardar" | Toast "Alumno actualizado" |
| 4 | Verificar tabla | Nombre cambiado |

**Resultado**: [ ] PASO / [ ] FALLO

#### Flujo UAT-03: Eliminacion con Confirmacion

| Paso | Accion | Verificar |
|------|--------|-----------|
| 1 | Click "Eliminar" en un alumno | Modal visible |
| 2 | Click "Cancelar" | Modal cierra, alumno persiste |
| 3 | Click "Eliminar" otra vez | Modal visible |
| 4 | Click "Si, Eliminar" | Toast "Alumno eliminado" |
| 5 | Verificar tabla | Alumno ya no aparece |

**Resultado**: [ ] PASO / [ ] FALLO

### B.4 Pruebas de Seguridad Manuales

#### Prueba: Sesion Expira

| Paso | Accion | Verificar |
|------|--------|-----------|
| 1 | Login exitoso | Timer visible (15:00) |
| 2 | Esperar 15 min sin actividad | Timer llega a 0:00 |
| 3 | Observar | Modal "Sesion Expirada" |
| 4 | Click en "Iniciar Sesion" | Redirige a login |

**Resultado**: [ ] PASO / [ ] FALLO

#### Prueba: API sin Token

| Paso | Accion | Verificar |
|------|--------|-----------|
| 1 | Abrir DevTools (F12) > Console | Consola visible |
| 2 | Ejecutar: `fetch('/api/alumnos')` | Promesa retornada |
| 3 | Ver Network | Status: 401 |

**Resultado**: [ ] PASO / [ ] FALLO

### B.5 Registro de Resultados UAT

| Flujo | Ejecutor | Fecha | Resultado | Observaciones |
|-------|----------|-------|-----------|---------------|
| UAT-01 | | | | |
| UAT-02 | | | | |
| UAT-03 | | | | |
| Sesion | | | | |
| API | | | | |

---

## Parte C: Criterios de Aceptacion Final

### C.1 Tests Automaticos

| Criterio | Requerido | Actual |
|----------|-----------|--------|
| Tests de Entidad | 15+ | Pendiente |
| Tests de Servicio | 15+ | Pendiente |
| Tests de API | 10+ | Pendiente |
| Cobertura minima | 60% | Pendiente |
| Tests fallidos | 0 | Pendiente |

### C.2 Validacion Manual UAT

| Criterio | Requerido | Actual |
|----------|-----------|--------|
| UAT-01 (Crear) | PASO | Pendiente |
| UAT-02 (Editar) | PASO | Pendiente |
| UAT-03 (Eliminar) | PASO | Pendiente |
| Sesion expira | PASO | Pendiente |
| API protegida | PASO | Pendiente |

---

## Parte D: Siguiente Paso

Una vez que:
- [ ] Todos los tests automaticos pasan (verde)
- [ ] Todos los flujos UAT pasan (humano verificado)

Entonces se puede proceder a:
- **Fase 6**: Despliegue a Produccion (Vercel)

---

> **Documento**: Manual de Ejecucion y Validacion  
> **Version**: 1.0.0
