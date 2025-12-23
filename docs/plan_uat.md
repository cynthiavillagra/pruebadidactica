# Plan de Pruebas de Aceptacion (UAT)

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Fase**: 5 - Testing Formal  
> **Fecha**: 2025-12-22

---

## 1. Introduccion

### 1.1 Proposito

Este documento define los **flujos de prueba de aceptacion** (UAT - User Acceptance Testing) que validan que el sistema cumple con los Criterios de Aceptacion definidos en las Historias de Usuario.

### 1.2 Alcance

Se prueban 3 flujos completos que cubren las funcionalidades CRUD principales:

| Flujo | Descripcion | HU Relacionada |
|-------|-------------|----------------|
| UAT-01 | Registro de nuevo alumno | HU-001 |
| UAT-02 | Edicion de alumno existente | HU-003 |
| UAT-03 | Eliminacion con confirmacion | HU-004 |

---

## 2. Precondiciones Generales

Antes de ejecutar cualquier flujo:

1. Servidor corriendo: `python api/index.py`
2. Usuario autenticado en Supabase
3. Navegador abierto en `http://localhost:5000`
4. Sesion activa (timer visible en header)

---

## 3. Flujo UAT-01: Registro de Nuevo Alumno

### 3.1 Trazabilidad

| Campo | Valor |
|-------|-------|
| **Historia de Usuario** | HU-001: Registrar Alumno |
| **Requisito Funcional** | RF-001, RF-005, RF-010 |
| **Criterios de Aceptacion** | CA-001.1, CA-001.2, CA-001.3 |

### 3.2 Pasos de Ejecucion

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Click en "Nuevo Alumno" | Se muestra formulario vacio |
| 2 | Ingresar nombre: "Maria" | Campo se completa |
| 3 | Ingresar apellido: "Garcia" | Campo se completa |
| 4 | Ingresar DNI: "33445566" | Campo se completa |
| 5 | Click en "Guardar" | Toast "Alumno creado correctamente" |
| 6 | Verificar tabla | Aparece "Garcia, Maria" en la lista |

### 3.3 Criterios de Aceptacion Verificados

| CA | Descripcion | Verificacion |
|----|-------------|--------------|
| CA-001.1 | Campos obligatorios requeridos | Form no envia si estan vacios |
| CA-001.2 | DNI unico | Error si DNI ya existe |
| CA-001.3 | Alumno aparece en lista | Tabla se actualiza |

### 3.4 Caso Negativo: DNI Duplicado

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Click en "Nuevo Alumno" | Formulario visible |
| 2 | Ingresar DNI existente | Campo se completa |
| 3 | Click en "Guardar" | Error: "El DNI ya esta registrado" |

---

## 4. Flujo UAT-02: Edicion de Alumno

### 4.1 Trazabilidad

| Campo | Valor |
|-------|-------|
| **Historia de Usuario** | HU-003: Editar Alumno |
| **Requisito Funcional** | RF-003, RF-005 |
| **Criterios de Aceptacion** | CA-003.1, CA-003.2 |

### 4.2 Precondiciones Especificas

- Existe al menos 1 alumno en la lista

### 4.3 Pasos de Ejecucion

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Click en "Editar" de un alumno | Formulario con datos cargados |
| 2 | Modificar nombre a "Maria Jose" | Campo se actualiza |
| 3 | Click en "Guardar" | Toast "Alumno actualizado" |
| 4 | Verificar tabla | Nombre actualizado en lista |

### 4.4 Criterios de Aceptacion Verificados

| CA | Descripcion | Verificacion |
|----|-------------|--------------|
| CA-003.1 | Datos pre-cargados | Formulario muestra valores actuales |
| CA-003.2 | Cambios persistidos | Tabla refleja los cambios |

---

## 5. Flujo UAT-03: Eliminacion con Confirmacion

### 5.1 Trazabilidad

| Campo | Valor |
|-------|-------|
| **Historia de Usuario** | HU-004: Eliminar Alumno |
| **Requisito Funcional** | RF-004, RF-009 |
| **Criterios de Aceptacion** | CA-004.1, CA-004.2 |

### 5.2 Precondiciones Especificas

- Existe al menos 1 alumno en la lista

### 5.3 Pasos de Ejecucion

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Click en "Eliminar" de un alumno | Modal de confirmacion visible |
| 2 | Verificar mensaje | "Seguro que desea eliminar a [Nombre]?" |
| 3 | Click en "Cancelar" | Modal se cierra, alumno persiste |
| 4 | Click en "Eliminar" nuevamente | Modal visible |
| 5 | Click en "Si, Eliminar" | Toast "Alumno eliminado" |
| 6 | Verificar tabla | Alumno ya no aparece |

### 5.4 Criterios de Aceptacion Verificados

| CA | Descripcion | Verificacion |
|----|-------------|--------------|
| CA-004.1 | Confirmacion requerida | Modal aparece antes de eliminar |
| CA-004.2 | Eliminacion completa | Alumno desaparece de la lista |

---

## 6. Pruebas de Sesion y Seguridad

### 6.1 Flujo UAT-04: Expiracion de Sesion

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Login exitoso | Pantalla principal visible |
| 2 | Esperar 15 minutos sin actividad | Timer llega a 0:00 |
| 3 | Observar pantalla | Modal "Sesion Expirada" |
| 4 | Click en "Iniciar Sesion" | Redirige a login |

### 6.2 Flujo UAT-05: Acceso sin Autenticacion

| Paso | Accion | Resultado Esperado |
|------|--------|-------------------|
| 1 | Abrir DevTools > Network | Panel visible |
| 2 | Hacer peticion a `/api/alumnos` sin token | Respuesta 401 |
| 3 | Verificar response | {"error": "Token requerido"} |

---

## 7. Matriz de Cobertura

| Historia | Criterio | UAT | Estado |
|----------|----------|-----|--------|
| HU-001 | CA-001.1 | UAT-01 | Pendiente |
| HU-001 | CA-001.2 | UAT-01 | Pendiente |
| HU-001 | CA-001.3 | UAT-01 | Pendiente |
| HU-003 | CA-003.1 | UAT-02 | Pendiente |
| HU-003 | CA-003.2 | UAT-02 | Pendiente |
| HU-004 | CA-004.1 | UAT-03 | Pendiente |
| HU-004 | CA-004.2 | UAT-03 | Pendiente |

---

## 8. Registro de Resultados

| Flujo | Fecha | Ejecutor | Resultado | Observaciones |
|-------|-------|----------|-----------|---------------|
| UAT-01 | | | | |
| UAT-02 | | | | |
| UAT-03 | | | | |
| UAT-04 | | | | |
| UAT-05 | | | | |

---

> **Documento**: Plan de Pruebas UAT  
> **Version**: 1.0.0
