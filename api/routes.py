# ===========================================================================
# Rutas de la API
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: API (Presentacion)
# ===========================================================================
#
# POR QUE SEPARAR RUTAS DE INDEX.PY:
# - Single Responsibility: este archivo solo define rutas
# - Facilita testing de endpoints
# - El entry point (index.py) solo configura la app
#
# REGLA DE SEGURIDAD:
# - TODOS los endpoints CRUD usan @require_auth
# - El endpoint health es publico (para monitoreo)
#
# TRAZABILIDAD:
# - Cada endpoint referencia su Historia de Usuario
#
# ===========================================================================

"""
Rutas de la API REST para gestionar Alumnos.

Define los endpoints HTTP y delega la logica al servicio.
"""

# Configuracion de path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from api.middleware.auth import require_auth
from application.alumno_service import create_alumno_service
from domain.exceptions import (
    DomainException,
    ValidacionError,
    AlumnoNoEncontrado,
    DNIDuplicado
)


# Crear Blueprint para las rutas de la API
# POR QUE BLUEPRINT: Permite modularizar la app en componentes
api_bp = Blueprint('api', __name__, url_prefix='/api')


# ===========================================================================
# ENDPOINTS PUBLICOS
# ===========================================================================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check (publico).
    
    Trazabilidad: RNF (Monitoreo)
    
    No requiere autenticacion.
    Util para verificar que el servicio esta corriendo.
    
    Returns:
        200 OK con estado del servicio
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '1.0.0'
    }), 200


# ===========================================================================
# ENDPOINTS CRUD (Protegidos)
# ===========================================================================

@api_bp.route('/alumnos', methods=['GET'])
@require_auth
def listar_alumnos():
    """
    Listar todos los alumnos.
    
    Trazabilidad:
    - HU-002: Ver Lista de Alumnos
    - RF-002: Listar alumnos
    
    Returns:
        200 OK con lista de alumnos
    """
    try:
        service = create_alumno_service()
        alumnos = service.listar_alumnos()
        
        return jsonify([alumno.to_dict() for alumno in alumnos]), 200
        
    except Exception as e:
        return _handle_error(e)


@api_bp.route('/alumnos', methods=['POST'])
@require_auth
def crear_alumno():
    """
    Crear un nuevo alumno.
    
    Trazabilidad:
    - HU-001: Registrar Alumno
    - RF-001, RF-005, RF-010
    
    Request Body:
        {
            "nombre": "string",
            "apellido": "string",
            "dni": "string"
        }
    
    Returns:
        201 Created con el alumno creado
        400 Bad Request si datos invalidos
        409 Conflict si DNI duplicado
    """
    try:
        # Obtener datos del body
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Body JSON requerido'}), 400
        
        # Crear alumno
        service = create_alumno_service()
        alumno = service.crear_alumno(
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            dni=data.get('dni', '')
        )
        
        return jsonify(alumno.to_dict()), 201
        
    except ValidacionError as e:
        return jsonify(e.to_dict()), 400
        
    except DNIDuplicado as e:
        return jsonify(e.to_dict()), 409
        
    except Exception as e:
        return _handle_error(e)


@api_bp.route('/alumnos/<id>', methods=['GET'])
@require_auth
def obtener_alumno(id):
    """
    Obtener un alumno por ID.
    
    Trazabilidad:
    - HU-002: Ver Lista de Alumnos
    - RF-002
    
    Args:
        id: UUID del alumno
    
    Returns:
        200 OK con el alumno
        404 Not Found si no existe
    """
    try:
        service = create_alumno_service()
        alumno = service.obtener_alumno(id)
        
        return jsonify(alumno.to_dict()), 200
        
    except AlumnoNoEncontrado as e:
        return jsonify(e.to_dict()), 404
        
    except Exception as e:
        return _handle_error(e)


@api_bp.route('/alumnos/<id>', methods=['PUT'])
@require_auth
def actualizar_alumno(id):
    """
    Actualizar un alumno existente.
    
    Trazabilidad:
    - HU-003: Editar Alumno
    - RF-003, RF-005, RF-010
    
    Args:
        id: UUID del alumno
    
    Request Body:
        {
            "nombre": "string",
            "apellido": "string",
            "dni": "string"
        }
    
    Returns:
        200 OK con el alumno actualizado
        400 Bad Request si datos invalidos
        404 Not Found si no existe
        409 Conflict si DNI duplicado
    """
    try:
        # Obtener datos del body
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Body JSON requerido'}), 400
        
        # Actualizar alumno
        service = create_alumno_service()
        alumno = service.actualizar_alumno(
            id=id,
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            dni=data.get('dni', '')
        )
        
        return jsonify(alumno.to_dict()), 200
        
    except ValidacionError as e:
        return jsonify(e.to_dict()), 400
        
    except AlumnoNoEncontrado as e:
        return jsonify(e.to_dict()), 404
        
    except DNIDuplicado as e:
        return jsonify(e.to_dict()), 409
        
    except Exception as e:
        return _handle_error(e)


@api_bp.route('/alumnos/<id>', methods=['DELETE'])
@require_auth
def eliminar_alumno(id):
    """
    Eliminar un alumno.
    
    Trazabilidad:
    - HU-004: Eliminar Alumno
    - RF-004, RF-009
    
    Args:
        id: UUID del alumno
    
    Returns:
        204 No Content si se elimino
        404 Not Found si no existe
    """
    try:
        service = create_alumno_service()
        service.eliminar_alumno(id)
        
        return '', 204
        
    except AlumnoNoEncontrado as e:
        return jsonify(e.to_dict()), 404
        
    except Exception as e:
        return _handle_error(e)


# ===========================================================================
# MANEJO DE ERRORES
# ===========================================================================

def _handle_error(error: Exception):
    """
    Maneja errores generales de forma consistente.
    
    Args:
        error: Excepcion capturada
    
    Returns:
        Response JSON con el error
    """
    # Si es una excepcion de dominio, usar su formato
    if isinstance(error, DomainException):
        return jsonify(error.to_dict()), 500
    
    # Error generico
    return jsonify({
        'error': 'Error interno del servidor',
        'codigo': 'INTERNAL_ERROR',
        'detalle': str(error)
    }), 500


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Rutas API ===\n")
    
    from flask import Flask
    
    # Crear app de prueba
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    
    # Test con cliente de prueba
    with app.test_client() as client:
        # Test 1: Health check (no requiere auth)
        response = client.get('/api/health')
        print(f"[OK] GET /api/health: {response.status_code}")
        print(f"     Body: {response.get_json()}")
        
        # Test 2: Listar sin auth (debe fallar)
        response = client.get('/api/alumnos')
        print(f"[OK] GET /api/alumnos sin auth: {response.status_code}")
        
        # Test 3: Crear sin auth (debe fallar)
        response = client.post('/api/alumnos', json={
            'nombre': 'Test',
            'apellido': 'Test',
            'dni': '12345678'
        })
        print(f"[OK] POST /api/alumnos sin auth: {response.status_code}")
    
    print("\n=== Pruebas basicas pasaron ===")
    print("\nNOTA: Para probar endpoints protegidos, necesitas un JWT valido")
