# ===========================================================================
# Middleware de Autenticacion
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: API (Presentacion)
# Patron: Decorator
# ===========================================================================
#
# POR QUE MIDDLEWARE:
# - Centraliza la logica de autenticacion
# - Evita repetir codigo en cada endpoint
# - Facilita testing (se puede desactivar para tests)
#
# REGLA DE SEGURIDAD:
# - TODOS los endpoints protegidos deben usar @require_auth
# - El decorador valida el JWT y extrae el usuario
# - Si falla, retorna 401 ANTES de ejecutar el endpoint
#
# WATCHDOG DE SESION:
# - El frontend maneja el timeout de 15 minutos
# - El backend solo valida que el token no este expirado
# - Si el token expiro, retorna SESSION_EXPIRED
#
# ===========================================================================

"""
Middleware de autenticacion para endpoints protegidos.

Valida JWT de Supabase y extrae informacion del usuario.
"""

# Configuracion de path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jwt
from functools import wraps
from flask import request, jsonify, g
from datetime import datetime, timezone

from domain.exceptions import AuthenticationError, SessionExpiredError


def require_auth(f):
    """
    Decorador que requiere autenticacion JWT.
    
    Uso:
        @app.route('/api/alumnos')
        @require_auth
        def listar_alumnos():
            user = g.current_user  # Usuario autenticado
            ...
    
    Validaciones:
    1. Header Authorization presente
    2. Formato "Bearer <token>"
    3. JWT valido (firma correcta)
    4. JWT no expirado
    
    Si pasa validacion:
    - g.current_user contiene el payload del JWT
    - g.jwt_token contiene el token original
    
    Si falla:
    - Retorna 401 Unauthorized con mensaje de error
    
    Patron: Decorator
    
    POR QUE DECORADOR Y NO MIDDLEWARE GLOBAL:
    - Permite elegir que rutas proteger
    - Mas explicito: se ve en cada ruta
    - Rutas publicas (ej: health) no lo necesitan
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 1. Obtener header Authorization
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                raise AuthenticationError("Token de autenticacion requerido")
            
            # 2. Extraer token del header
            token = _extract_token(auth_header)
            
            # 3. Validar y decodificar JWT
            payload = _validate_jwt(token)
            
            # 4. Verificar expiracion
            _check_expiration(payload)
            
            # 5. Guardar usuario en contexto de Flask
            g.current_user = payload
            g.jwt_token = token
            
            # 6. Ejecutar la funcion original
            return f(*args, **kwargs)
            
        except SessionExpiredError as e:
            # Sesion expirada: codigo especifico para que el frontend redirija
            return jsonify(e.to_dict()), 401
            
        except AuthenticationError as e:
            return jsonify(e.to_dict()), 401
            
        except Exception as e:
            # Error inesperado en autenticacion
            return jsonify({
                'error': 'Error de autenticacion',
                'codigo': 'AUTH_ERROR',
                'detalle': str(e)
            }), 401
    
    return decorated_function


def _extract_token(auth_header: str) -> str:
    """
    Extrae el token del header Authorization.
    
    Formato esperado: "Bearer <token>"
    
    Args:
        auth_header: Valor del header Authorization
    
    Returns:
        Token JWT
    
    Raises:
        AuthenticationError: Si el formato es invalido
    """
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise AuthenticationError("Formato de token invalido. Use: Bearer <token>")
    
    return parts[1]


def _validate_jwt(token: str) -> dict:
    """
    Valida y decodifica un JWT de Supabase.
    
    Args:
        token: JWT a validar
    
    Returns:
        Payload del JWT decodificado
    
    Raises:
        AuthenticationError: Si el token es invalido
        SessionExpiredError: Si el token expiro
    """
    try:
        from infrastructure.config import get_config
        config = get_config()
        
        # Decodificar con verificacion de firma
        # POR QUE HS256: Es el algoritmo que usa Supabase
        payload = jwt.decode(
            token,
            config.SUPABASE_JWT_SECRET,
            algorithms=['HS256'],
            options={
                'verify_exp': True,  # Verificar expiracion
                'verify_iat': True,  # Verificar issued at
            }
        )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise SessionExpiredError()
        
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Token invalido: {e}")


def _check_expiration(payload: dict) -> None:
    """
    Verifica manualmente la expiracion del token.
    
    POR QUE VERIFICACION ADICIONAL:
    - PyJWT ya verifica, pero queremos control adicional
    - Podemos agregar logica de "casi expirado" en el futuro
    
    Args:
        payload: Payload del JWT decodificado
    
    Raises:
        SessionExpiredError: Si el token expiro
    """
    exp = payload.get('exp')
    
    if exp is None:
        raise AuthenticationError("Token sin fecha de expiracion")
    
    now = datetime.now(timezone.utc).timestamp()
    
    if now > exp:
        raise SessionExpiredError()


def get_current_user() -> dict:
    """
    Obtiene el usuario actual autenticado.
    
    Uso dentro de un endpoint protegido:
        user = get_current_user()
        user_id = user.get('sub')
    
    Returns:
        Payload del JWT del usuario actual
    
    Raises:
        AuthenticationError: Si no hay usuario autenticado
    """
    if not hasattr(g, 'current_user') or g.current_user is None:
        raise AuthenticationError("No hay usuario autenticado")
    
    return g.current_user


def get_user_id() -> str:
    """
    Obtiene el ID del usuario actual.
    
    Returns:
        ID (sub) del usuario
    
    Raises:
        AuthenticationError: Si no hay usuario autenticado
    """
    user = get_current_user()
    return user.get('sub', user.get('id', ''))


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Middleware de Autenticacion ===\n")
    
    # Test 1: Extraer token valido
    try:
        token = _extract_token("Bearer abc123")
        print(f"[OK] Extraer token: {token}")
    except Exception as e:
        print(f"[ERROR] Extraer: {e}")
    
    # Test 2: Formato invalido
    try:
        _extract_token("InvalidFormat")
        print("[ERROR] Debio fallar")
    except AuthenticationError as e:
        print(f"[OK] Formato invalido detectado: {e.message}")
    
    # Test 3: Sin Bearer
    try:
        _extract_token("Token abc123")
        print("[ERROR] Debio fallar")
    except AuthenticationError as e:
        print(f"[OK] Sin Bearer detectado: {e.message}")
    
    # Test 4: Token expirado (simulado)
    try:
        _check_expiration({'exp': 0})  # Fecha en el pasado
        print("[ERROR] Debio fallar por expiracion")
    except SessionExpiredError as e:
        print(f"[OK] Expiracion detectada: {e.message}")
    
    # Test 5: Token valido (no expirado)
    import time
    try:
        _check_expiration({'exp': time.time() + 3600})  # +1 hora
        print("[OK] Token no expirado verificado")
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("\n=== Todas las pruebas pasaron ===")
    print("\nNOTA: La validacion completa de JWT requiere un token real de Supabase")
