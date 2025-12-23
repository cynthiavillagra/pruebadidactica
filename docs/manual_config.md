# Manual Tecnico: infrastructure/config.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Infrastructure (Capa de Infraestructura)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo centraliza la **carga y validacion de variables de entorno**. Todas las configuraciones sensibles (credenciales Supabase, secretos Flask) se leen desde el archivo `.env` y se validan al iniciar la aplicacion.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Infrastructure Layer |
| **Requisitos No Funcionales** | RNF-005 (Datos protegidos) |
| **Patron** | Configuration Object, 12-Factor App |

### 1.3 Por Que Configuracion Centralizada

**SI se eligio**:
- Una unica fuente de verdad para config
- Validacion al inicio (fail-fast)
- Valores tipados (no strings crudos)
- Valores por defecto seguros

**NO se eligio**:
- `os.getenv()` disperso en el codigo
- Sin validacion de variables requeridas
- Hardcodear valores en el codigo

---

## 2. Estrategia de Construccion

### 2.1 Variables de Entorno

| Variable | Requerida | Default | Uso |
|----------|-----------|---------|-----|
| `SUPABASE_URL` | SI | - | URL del proyecto Supabase |
| `SUPABASE_KEY` | SI | - | API Key publica (anon) |
| `SUPABASE_JWT_SECRET` | SI | - | Secret para validar JWT |
| `FLASK_ENV` | NO | development | Modo de Flask |
| `FLASK_DEBUG` | NO | 1 | Debug activado |
| `FLASK_SECRET_KEY` | NO | auto | Secret de sesiones |
| `PORT` | NO | 5000 | Puerto del servidor |
| `SESSION_TIMEOUT_SECONDS` | NO | 900 | Timeout de sesion |

### 2.2 Clase Config

```python
class Config:
    # Supabase (REQUERIDAS)
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    # Flask (OPCIONALES)
    FLASK_ENV: str = 'development'
    FLASK_DEBUG: bool = True
    FLASK_SECRET_KEY: str
    PORT: int = 5000
    SESSION_TIMEOUT_SECONDS: int = 900
```

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Intenta cargar la configuracion
2. Si `.env` existe, muestra que se cargo bien
3. Si no existe, muestra advertencia (esperado sin `.env`)

### 3.2 Funcion get_config()

```python
_config_instance: Optional[Config] = None

def get_config() -> Config:
    """Retorna la configuracion (singleton)."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
```

**Por que Singleton**:
- Carga `.env` solo una vez
- Validacion solo al inicio
- Consistencia en toda la app

---

## 4. Codigo Fuente

### 4.1 Carga de dotenv

```python
from dotenv import load_dotenv

# Cargar .env al importar el modulo
load_dotenv()
```

### 4.2 Validacion de Requeridas

```python
def __init__(self):
    self.SUPABASE_URL = self._get_required('SUPABASE_URL')
    self.SUPABASE_KEY = self._get_required('SUPABASE_KEY')
    self.SUPABASE_JWT_SECRET = self._get_required('SUPABASE_JWT_SECRET')

def _get_required(self, name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Variable de entorno '{name}' no configurada")
    return value
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python infrastructure/config.py
```

### 5.2 Salida Esperada (con .env)

```
=== Prueba de Configuracion ===

[OK] Configuracion cargada correctamente
     SUPABASE_URL: https://xxx.supabase.co
     FLASK_ENV: development
     PORT: 5000
```

### 5.3 Salida Esperada (sin .env)

```
=== Prueba de Configuracion ===

[ADVERTENCIA] Variable de entorno 'SUPABASE_URL' no configurada

Esto es esperado si no tienes .env configurado.
```

### 5.4 Unit Test Rapido

```python
def test_config_requiere_supabase_url():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError):
            Config()
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| `load_dotenv()` al inicio | Variables disponibles inmediatamente |
| Singleton | Una sola carga de config |
| Fail-fast | Error claro si falta variable |
| Tipos convertidos | `int()` para PORT, `bool` para DEBUG |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Config en JSON/YAML | Menos seguro para secretos |
| Variables en codigo | Exposicion de credenciales |
| Sin validacion | Errores tardios, dificiles de debugear |
| Multiples archivos .env | Complejidad innecesaria |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `EnvironmentError: SUPABASE_URL` | Falta .env | `copy .env.example .env` y editar |
| Config vacia | .env no cargado | Verificar que load_dotenv() se ejecuta |
| Puerto en uso | PORT ocupado | Cambiar PORT en .env |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel/Nube |
|---------|-------|-------------|
| Fuente de variables | `.env` archivo | Dashboard/Secrets |
| `load_dotenv()` | Necesario | Ignorado (no hay .env) |
| Debug | Activado | Desactivado |
| FLASK_ENV | development | production |

---

> **Manual Tecnico**: infrastructure/config.py  
> **Version**: 1.0.0
