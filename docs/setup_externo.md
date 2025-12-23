# Guia de Configuracion de APIs Externas

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Fase**: 4-A (Setup)  
> **Fecha**: 2025-12-22

---

## Indice

1. [Configuracion de Supabase](#1-configuracion-de-supabase)
2. [Obtencion de Credenciales](#2-obtencion-de-credenciales)
3. [Configuracion del Archivo .env](#3-configuracion-del-archivo-env)
4. [Verificacion de Conexion](#4-verificacion-de-conexion)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Configuracion de Supabase

### 1.1 Crear Cuenta

1. Ir a [https://supabase.com](https://supabase.com)
2. Click en **Start your project**
3. Iniciar sesion con GitHub (recomendado) o email

### 1.2 Crear Proyecto

1. Click en **New Project**
2. Completar:
   - **Name**: `app-didactica-crud` (o el nombre que prefieras)
   - **Database Password**: Genera una contrasena segura y GUARDALA
   - **Region**: `South America (Sao Paulo)` (mas cercano a Argentina)
3. Click en **Create new project**
4. Esperar ~2 minutos a que se aprovisione

### 1.3 Crear Tabla de Alumnos

1. Ir a **SQL Editor** (icono de base de datos)
2. Click en **New Query**
3. Copiar el contenido de `database/init.sql`
4. Click en **Run** (o Ctrl+Enter)
5. Verificar mensaje de exito

---

## 2. Obtencion de Credenciales

### 2.1 Donde Encontrar las Credenciales

1. En el dashboard de Supabase, ir a **Settings** (icono de engranaje)
2. Click en **API** en el menu lateral

### 2.2 Credenciales Necesarias

| Credencial | Donde Encontrar | Uso |
|------------|-----------------|-----|
| **Project URL** | API Settings > Project URL | `SUPABASE_URL` |
| **anon public** | API Settings > Project API keys | `SUPABASE_KEY` |
| **JWT Secret** | API Settings > JWT Settings | `SUPABASE_JWT_SECRET` |

### 2.3 Captura de Pantalla (Referencia)

```
Settings > API
|
|-- Project URL
|   https://xxxxxxxxxxxxx.supabase.co  <-- Copiar esto
|
|-- Project API keys
|   |-- anon (public)
|   |   eyJhbGciOiJIUzI1NiIsInR5cCI6...  <-- Copiar esto
|   |
|   |-- service_role (secret)
|       [NO USAR ESTA - es de administrador]
|
|-- JWT Settings
    |-- JWT Secret
        your-super-secret-jwt-token  <-- Copiar esto
```

---

## 3. Configuracion del Archivo .env

### 3.1 Crear Archivo .env

```powershell
# En la raiz del proyecto
copy .env.example .env
```

### 3.2 Editar con tus Credenciales

Abrir `.env` en un editor y reemplazar los placeholders:

```env
# SUPABASE
SUPABASE_URL=https://TU-PROYECTO-ID.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.TU-ANON-KEY
SUPABASE_JWT_SECRET=TU-JWT-SECRET

# FLASK
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=genera-una-clave-con-python-secrets
PORT=5000

# SEGURIDAD
SESSION_TIMEOUT_SECONDS=900
```

### 3.3 Generar FLASK_SECRET_KEY

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiar el resultado y pegarlo en `FLASK_SECRET_KEY`.

---

## 4. Verificacion de Conexion

### 4.1 Test de Configuracion

```powershell
python infrastructure/config.py
```

Salida esperada:
```
=== Prueba de Configuracion ===
[OK] Configuracion cargada correctamente
```

### 4.2 Test de Cliente Supabase

```powershell
python infrastructure/supabase_client.py
```

Salida esperada:
```
=== Prueba de Cliente Supabase ===
[OK] Cliente Supabase creado correctamente
[OK] Es singleton: True
[OK] Conexion a Supabase verificada
```

### 4.3 Test de Repositorio

```powershell
python infrastructure/supabase_alumno_repository.py
```

Salida esperada:
```
=== Prueba de SupabaseAlumnoRepository ===
[OK] Repositorio creado
[OK] Listar alumnos: X encontrados
```

---

## 5. Troubleshooting

### Error: "Variable de entorno 'X' no configurada"

**Causa**: Falta el archivo `.env` o alguna variable.

**Solucion**:
1. Verificar que `.env` existe en la raiz
2. Verificar que tiene todas las variables de `.env.example`
3. Verificar que no hay espacios extra

### Error: "Invalid API key"

**Causa**: La API key de Supabase es incorrecta.

**Solucion**:
1. Ir a Supabase > Settings > API
2. Copiar nuevamente la key `anon public`
3. Verificar que no hay espacios ni saltos de linea

### Error: "JWT signature verification failed"

**Causa**: El JWT Secret es incorrecto.

**Solucion**:
1. Ir a Supabase > Settings > API > JWT Settings
2. Copiar el JWT Secret correcto
3. Verificar que es el secret, no la key

### Error: "relation 'alumnos' does not exist"

**Causa**: La tabla no fue creada en Supabase.

**Solucion**:
1. Ir a SQL Editor en Supabase
2. Ejecutar el script `database/init.sql`
3. Verificar que no hubo errores

### Error: "new row violates row-level security policy"

**Causa**: RLS esta activo pero no hay politicas.

**Solucion**:
1. Verificar que el script `init.sql` incluyo las politicas RLS
2. O temporalmente: `ALTER TABLE alumnos DISABLE ROW LEVEL SECURITY;`

---

## Resumen de Verificacion

| Paso | Comando | Resultado Esperado |
|------|---------|-------------------|
| 1 | `python infrastructure/config.py` | "[OK] Configuracion cargada" |
| 2 | `python infrastructure/supabase_client.py` | "[OK] Cliente creado" |
| 3 | `python infrastructure/supabase_alumno_repository.py` | "[OK] Listar alumnos" |
| 4 | `python api/index.py` | Servidor en http://localhost:5000 |

---

> **Documento**: Guia de APIs Externas  
> **Version**: 1.0.0
