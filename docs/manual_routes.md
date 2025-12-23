# Manual Tecnico: api/routes.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: API (Capa de Presentacion - Rutas)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo define las **rutas de la API REST**. Cada endpoint recibe peticiones HTTP, las valida, llama al servicio correspondiente, y retorna respuestas JSON con codigos HTTP apropiados.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | API Layer - Routes |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004 |
| **Requisitos Funcionales** | RF-001 a RF-010 |
| **Patron** | Blueprint (Flask), RESTful |

### 1.3 Por Que Blueprint

**SI se eligio**:
- Modulariza las rutas de la API
- Separacion del entry point (index.py)
- Prefijo `/api` centralizado
- Facilita testing

**NO se eligio**:
- Rutas directas en index.py (monolitico)
- Multiples blueprints (overkill)
- Sin estructura REST

---

## 2. Estrategia de Construccion

### 2.1 Endpoints Definidos

| Metodo | Ruta | Funcion | Auth | HU |
|--------|------|---------|------|-----|
| GET | `/api/health` | health_check | No | - |
| GET | `/api/config` | get_config | No | - |
| GET | `/api/alumnos` | listar_alumnos | Si | HU-002 |
| POST | `/api/alumnos` | crear_alumno | Si | HU-001 |
| GET | `/api/alumnos/<id>` | obtener_alumno | Si | HU-002 |
| PUT | `/api/alumnos/<id>` | actualizar_alumno | Si | HU-003 |
| DELETE | `/api/alumnos/<id>` | eliminar_alumno | Si | HU-004 |

### 2.2 Codigos HTTP

| Codigo | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | GET, PUT exitosos |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 400 | Bad Request | Validacion fallida |
| 401 | Unauthorized | Sin auth o expirada |
| 404 | Not Found | ID no existe |
| 409 | Conflict | DNI duplicado |
| 500 | Server Error | Error interno |

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta una **prueba atomica** usando `test_client` de Flask:
1. Prueba GET /api/health (sin auth)
2. Prueba GET /api/alumnos sin auth (debe ser 401)
3. Prueba POST /api/alumnos sin auth (debe ser 401)

### 3.2 Manejo de Errores

```python
try:
    alumno = service.crear_alumno(...)
    return jsonify(alumno.to_dict()), 201
except ValidacionError as e:
    return jsonify(e.to_dict()), 400
except DNIDuplicado as e:
    return jsonify(e.to_dict()), 409
except Exception as e:
    return _handle_error(e)
```

---

## 4. Codigo Fuente

### 4.1 Blueprint

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')
```

### 4.2 Endpoint Publico

```python
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200
```

### 4.3 Endpoint Protegido

```python
@api_bp.route('/alumnos', methods=['GET'])
@require_auth
def listar_alumnos():
    service = create_alumno_service()
    alumnos = service.listar_alumnos()
    return jsonify([a.to_dict() for a in alumnos]), 200
```

### 4.4 Endpoint /api/config

```python
@api_bp.route('/config', methods=['GET'])
def get_config():
    """
    Retorna configuracion publica para el frontend.
    NO expone JWT_SECRET.
    """
    return jsonify({
        'supabase_url': os.getenv('SUPABASE_URL', ''),
        'supabase_key': os.getenv('SUPABASE_KEY', ''),
        'session_timeout': int(os.getenv('SESSION_TIMEOUT_SECONDS', '900'))
    }), 200
```

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python api/routes.py
```

### 5.2 Salida Esperada

```
=== Prueba de Rutas API ===

[OK] GET /api/health: 200
     Body: {'status': 'healthy', 'timestamp': '...', 'version': '1.0.0'}
[OK] GET /api/alumnos sin auth: 401
[OK] POST /api/alumnos sin auth: 401

=== Pruebas basicas pasaron ===

NOTA: Para probar endpoints protegidos, necesitas un JWT valido
```

### 5.3 Unit Test Rapido

```python
def test_health_retorna_200(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Blueprint | Modularidad |
| Prefijo /api | Separacion de estaticos |
| @require_auth explicito | Control granular |
| to_dict() en response | Serializacion limpia |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Flask-RESTful | Dependencia extra |
| Marshmallow schemas | Overkill para esta app |
| Rutas en index.py | Archivo muy largo |
| Autenticacion implicita | Menos claro |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| 404 en /api/alumnos | Blueprint no registrado | Verificar index.py |
| 401 siempre | Token invalido/faltante | Verificar header |
| 500 interno | Error en servicio/repo | Ver logs |

### 7.2 Prueba Manual con cURL

```powershell
# Health check
curl http://localhost:5000/api/health

# Config
curl http://localhost:5000/api/config

# Listar (requiere token)
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/alumnos

# Crear
curl -X POST -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"nombre":"Juan","apellido":"Perez","dni":"12345678"}' \
     http://localhost:5000/api/alumnos
```

---

> **Manual Tecnico**: api/routes.py  
> **Version**: 1.0.0
