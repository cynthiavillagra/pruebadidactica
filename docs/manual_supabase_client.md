# Manual Tecnico: infrastructure/supabase_client.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Infrastructure (Capa de Infraestructura)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo implementa el **cliente Supabase como Singleton**. Garantiza que exista una unica instancia del cliente en toda la aplicacion, optimizando recursos y conexiones.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Infrastructure Layer |
| **Requisitos No Funcionales** | RNF-001 (Performance) |
| **Patron** | Singleton, Lazy Initialization |

### 1.3 Por Que Singleton

**SI se eligio**:
- Una sola conexion a Supabase
- Reutilizacion eficiente
- Thread-safe para multiples requests
- Compatible con serverless

**NO se eligio**:
- Crear cliente en cada request (ineficiente)
- Variable global sin control
- Pool de conexiones (overkill para esta app)

---

## 2. Estrategia de Construccion

### 2.1 Patron Singleton Thread-Safe

```python
import threading

_client_instance: Optional[Client] = None
_lock = threading.Lock()

def get_supabase_client() -> Client:
    global _client_instance
    
    if _client_instance is None:
        with _lock:  # Thread-safe
            if _client_instance is None:  # Double-check
                _client_instance = _create_client()
    
    return _client_instance
```

### 2.2 Lazy Initialization

El cliente se crea **solo cuando se necesita** (no al importar el modulo):
- Evita errores si config no esta lista
- Reduce tiempo de startup
- Adecuado para serverless

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Obtiene el cliente
2. Verifica que es singleton (misma instancia)
3. Intenta una operacion simple (si .env esta configurado)

### 3.2 Por Que Thread-Safe

```python
with _lock:
    if _client_instance is None:
        _client_instance = _create_client()
```

**Escenario**: Dos requests llegan simultaneamente:
- Sin lock: Ambos crean cliente (desperdicio)
- Con lock: Solo uno crea, el otro espera y reutiliza

---

## 4. Codigo Fuente

### 4.1 Funcion Principal

```python
def get_supabase_client() -> Client:
    """
    Obtiene la instancia unica del cliente Supabase.
    
    POR QUE SINGLETON:
    - Una sola conexion a BD
    - Eficiente en memoria
    - Thread-safe
    
    Returns:
        Client de Supabase
    """
    global _client_instance
    
    if _client_instance is None:
        with _lock:
            if _client_instance is None:
                from infrastructure.config import get_config
                config = get_config()
                
                _client_instance = create_client(
                    config.SUPABASE_URL,
                    config.SUPABASE_KEY
                )
    
    return _client_instance
```

### 4.2 Funcion de Reset (para testing)

```python
def reset_client():
    """Resetea el singleton (solo para testing)."""
    global _client_instance
    _client_instance = None
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python infrastructure/supabase_client.py
```

### 5.2 Salida Esperada (con .env)

```
=== Prueba de Cliente Supabase ===

[OK] Cliente Supabase creado correctamente
[OK] Es singleton: True
[OK] Conexion a Supabase verificada

=== Prueba pasada ===
```

### 5.3 Salida Esperada (sin .env)

```
=== Prueba de Cliente Supabase ===

[ADVERTENCIA] Variable de entorno 'SUPABASE_URL' no configurada

Esto es esperado si no tienes .env configurado.
```

### 5.4 Unit Test Rapido

```python
def test_singleton_retorna_misma_instancia():
    client1 = get_supabase_client()
    client2 = get_supabase_client()
    assert client1 is client2
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Singleton | Una conexion, multiples usos |
| Lazy init | Solo crea cuando se necesita |
| Thread-safe | Seguro en multithreading |
| Double-check locking | Optimiza verificaciones |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Variable global directa | Sin control de inicializacion |
| Cliente por request | Ineficiente, conexiones multiples |
| Connection pool | Complejidad innecesaria |
| Cliente en modulo | Se crea al importar (puede fallar) |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `EnvironmentError` | Config no cargada | Verificar .env |
| `APIError` | Credenciales invalidas | Verificar SUPABASE_URL/KEY |
| `ConnectionError` | Sin internet | Verificar red |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel/Nube |
|---------|-------|-------------|
| Singleton | Persiste mientras corre | Puede recrearse |
| Conexion | Unica para toda la sesion | Por invocacion |
| Cold start | No aplica | Singleton se recrea |

### 7.3 Comportamiento Serverless

En serverless (Vercel):
- Cada instancia de funcion tiene su propio singleton
- El singleton persiste entre requests de la misma instancia
- Si la instancia "duerme", se recrea en el proximo request

---

> **Manual Tecnico**: infrastructure/supabase_client.py  
> **Version**: 1.0.0
