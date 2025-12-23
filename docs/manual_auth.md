# Manual Tecnico: api/middleware/auth.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: API (Capa de Presentacion - Middleware)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo implementa el **middleware de autenticacion**. Proporciona el decorador `@require_auth` que valida el JWT de Supabase antes de permitir acceso a endpoints protegidos.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | API Layer - Middleware |
| **Requisitos No Funcionales** | RNF-005 (Datos protegidos), RNF-008 (Sesion segura) |
| **Patron** | Decorator Pattern |

### 1.3 Por Que Decorador

**SI se eligio**:
- Reutilizable en cualquier endpoint
- Explicito: se ve en cada ruta
- Separa logica de auth de negocio
- Permite rutas publicas (sin decorador)

**NO se eligio**:
- Middleware global (protege todo, incluido health)
- Verificar en cada funcion manualmente
- Sesiones server-side (no stateless)

---

## 2. Estrategia de Construccion

### 2.1 Flujo del Decorador

```
Request --> @require_auth
            |
            v
        [Verificar Header Authorization?]
            |
            No --> 401 "Token requerido"
            |
            Si --> [Extraer Bearer token]
                   |
                   v
               [Validar JWT (firma)?]
                   |
                   No --> 401 "Token invalido"
                   |
                   Si --> [Verificar expiracion?]
                          |
                          Expirado --> 401 "SESSION_EXPIRED"
                          |
                          OK --> g.current_user = payload
                                 |
                                 v
                          [Ejecutar funcion original]
```

### 2.2 Validaciones

| Validacion | Error | Codigo HTTP |
|------------|-------|-------------|
| Header faltante | "Token requerido" | 401 |
| Formato invalido | "Use Bearer <token>" | 401 |
| Firma invalida | "Token invalido" | 401 |
| Token expirado | "SESSION_EXPIRED" | 401 |

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** que:
1. Prueba extraccion de token
2. Prueba deteccion de formato invalido
3. Prueba deteccion de expiracion

**No requiere .env** porque no valida JWT real.

### 3.2 Contexto de Flask

```python
g.current_user = payload  # Usuario disponible en la request
g.jwt_token = token       # Token original
```

**Uso en endpoint**:
```python
@app.route('/api/alumnos')
@require_auth
def listar():
    user = g.current_user  # Payload del JWT
    user_id = user.get('sub')
```

---

## 4. Codigo Fuente

### 4.1 Decorador Principal

```python
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                raise AuthenticationError("Token requerido")
            
            token = _extract_token(auth_header)
            payload = _validate_jwt(token)
            _check_expiration(payload)
            
            g.current_user = payload
            g.jwt_token = token
            
            return f(*args, **kwargs)
            
        except SessionExpiredError as e:
            return jsonify(e.to_dict()), 401
        except AuthenticationError as e:
            return jsonify(e.to_dict()), 401
    
    return decorated_function
```

### 4.2 Validacion de JWT

```python
def _validate_jwt(token: str) -> dict:
    from infrastructure.config import get_config
    config = get_config()
    
    payload = jwt.decode(
        token,
        config.SUPABASE_JWT_SECRET,
        algorithms=['HS256']
    )
    
    return payload
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python api/middleware/auth.py
```

### 5.2 Salida Esperada

```
=== Prueba de Middleware de Autenticacion ===

[OK] Extraer token: abc123
[OK] Formato invalido detectado: Use Bearer <token>
[OK] Sin Bearer detectado: Use Bearer <token>
[OK] Expiracion detectada: Sesion expirada
[OK] Token no expirado verificado

=== Todas las pruebas pasaron ===

NOTA: La validacion completa de JWT requiere un token real de Supabase
```

### 5.3 Unit Test Rapido

```python
def test_extract_token_valido():
    token = _extract_token("Bearer abc123")
    assert token == "abc123"

def test_extract_token_invalido():
    with pytest.raises(AuthenticationError):
        _extract_token("InvalidFormat")
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Decorador no global | Permite rutas publicas |
| SESSION_EXPIRED especifico | Frontend sabe que redirigir |
| JWT decode con PyJWT | Libreria estandar y segura |
| HS256 | Algoritmo que usa Supabase |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Sesiones server-side | Viola regla stateless |
| Middleware global | Bloquea health, config |
| Validar en cada funcion | Codigo repetitivo |
| Solo verificar presencia | Sin verificar firma (inseguro) |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `jwt.InvalidTokenError` | Token malformado | Verificar login |
| `jwt.ExpiredSignatureError` | Token expirado | Re-login |
| `SESSION_EXPIRED` | Inactividad | Re-login |
| `Token requerido` | Sin header | Agregar Authorization |

### 7.2 Prueba Manual con cURL

```powershell
# Sin token (debe fallar)
curl http://localhost:5000/api/alumnos

# Con token invalido (debe fallar)
curl -H "Authorization: Bearer invalid" http://localhost:5000/api/alumnos

# Con token valido (debe funcionar)
curl -H "Authorization: Bearer <token-real>" http://localhost:5000/api/alumnos
```

---

> **Manual Tecnico**: api/middleware/auth.py  
> **Version**: 1.0.0
