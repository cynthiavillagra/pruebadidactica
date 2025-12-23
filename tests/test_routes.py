# ===========================================================================
# Tests de las Rutas de la API
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Fase: 5 - Testing Formal
# ===========================================================================
#
# REGLAS DE TESTING:
# - Sin credenciales reales
# - Usa test_client de Flask
# - Mockea la autenticacion donde es necesario
#
# ===========================================================================

"""
Tests de integracion para los endpoints de la API.

Usa el test client de Flask para simular peticiones HTTP.
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Configuracion de path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def app():
    """Fixture que crea la aplicacion Flask para testing."""
    # Mockear la configuracion antes de importar
    with patch.dict('os.environ', {
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_KEY': 'test-key',
        'SUPABASE_JWT_SECRET': 'test-secret',
        'FLASK_ENV': 'testing',
        'FLASK_DEBUG': '0'
    }):
        from api.index import create_app
        app = create_app()
        app.config['TESTING'] = True
        yield app


@pytest.fixture
def client(app):
    """Fixture que crea el test client."""
    return app.test_client()


class TestHealthEndpoint:
    """Tests del endpoint de health check."""
    
    def test_health_retorna_200(self, client):
        """Verifica que /api/health retorna 200 OK."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
    
    def test_health_retorna_status_healthy(self, client):
        """Verifica que health retorna status healthy."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert data['status'] == 'healthy'
    
    def test_health_incluye_timestamp(self, client):
        """Verifica que health incluye timestamp."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'timestamp' in data
    
    def test_health_no_requiere_auth(self, client):
        """Verifica que health no requiere autenticacion."""
        # No enviamos header Authorization
        response = client.get('/api/health')
        
        # Debe funcionar igual
        assert response.status_code == 200


class TestConfigEndpoint:
    """Tests del endpoint de configuracion."""
    
    def test_config_retorna_200(self, client):
        """Verifica que /api/config retorna 200 OK."""
        response = client.get('/api/config')
        
        assert response.status_code == 200
    
    def test_config_retorna_supabase_url(self, client):
        """Verifica que config retorna supabase_url."""
        response = client.get('/api/config')
        data = response.get_json()
        
        assert 'supabase_url' in data
    
    def test_config_retorna_supabase_key(self, client):
        """Verifica que config retorna supabase_key."""
        response = client.get('/api/config')
        data = response.get_json()
        
        assert 'supabase_key' in data
    
    def test_config_no_expone_jwt_secret(self, client):
        """Verifica que config NO expone el JWT secret."""
        response = client.get('/api/config')
        data = response.get_json()
        
        # El JWT secret NUNCA debe exponerse
        assert 'jwt_secret' not in data
        assert 'supabase_jwt_secret' not in data


class TestAlumnosEndpointsSinAuth:
    """Tests de endpoints protegidos SIN autenticacion."""
    
    def test_listar_sin_auth_retorna_401(self, client):
        """Verifica que listar sin token retorna 401."""
        response = client.get('/api/alumnos')
        
        assert response.status_code == 401
    
    def test_crear_sin_auth_retorna_401(self, client):
        """Verifica que crear sin token retorna 401."""
        response = client.post('/api/alumnos', json={
            'nombre': 'Test',
            'apellido': 'Test',
            'dni': '12345678'
        })
        
        assert response.status_code == 401
    
    def test_obtener_sin_auth_retorna_401(self, client):
        """Verifica que obtener sin token retorna 401."""
        response = client.get('/api/alumnos/some-id')
        
        assert response.status_code == 401
    
    def test_actualizar_sin_auth_retorna_401(self, client):
        """Verifica que actualizar sin token retorna 401."""
        response = client.put('/api/alumnos/some-id', json={
            'nombre': 'Test',
            'apellido': 'Test',
            'dni': '12345678'
        })
        
        assert response.status_code == 401
    
    def test_eliminar_sin_auth_retorna_401(self, client):
        """Verifica que eliminar sin token retorna 401."""
        response = client.delete('/api/alumnos/some-id')
        
        assert response.status_code == 401


class TestAlumnosEndpointsConAuthMockeada:
    """Tests de endpoints con autenticacion mockeada."""
    
    @pytest.fixture
    def auth_headers(self):
        """Headers con token de autenticacion mock."""
        return {'Authorization': 'Bearer mock-token'}
    
    @pytest.fixture
    def mock_auth(self):
        """Fixture que mockea la validacion de auth."""
        with patch('api.middleware.auth._validate_jwt') as mock:
            mock.return_value = {
                'sub': 'user-123',
                'email': 'test@test.com',
                'exp': datetime.now(timezone.utc).timestamp() + 3600
            }
            yield mock
    
    @pytest.fixture
    def mock_service(self):
        """Fixture que mockea el servicio de alumnos."""
        with patch('api.routes.create_alumno_service') as mock:
            service_mock = MagicMock()
            mock.return_value = service_mock
            yield service_mock
    
    def test_listar_con_auth_mock_retorna_200(self, client, auth_headers, mock_auth, mock_service):
        """Verifica que listar con auth valida retorna 200."""
        # Configurar mock del servicio
        mock_service.listar_alumnos.return_value = []
        
        # Act
        response = client.get('/api/alumnos', headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
    
    def test_listar_retorna_lista_json(self, client, auth_headers, mock_auth, mock_service):
        """Verifica que listar retorna una lista JSON."""
        mock_service.listar_alumnos.return_value = []
        
        response = client.get('/api/alumnos', headers=auth_headers)
        data = response.get_json()
        
        assert isinstance(data, list)


class TestFormatosDeRespuesta:
    """Tests de formatos de respuesta."""
    
    def test_health_es_json(self, client):
        """Verifica que health retorna JSON."""
        response = client.get('/api/health')
        
        assert response.content_type == 'application/json'
    
    def test_error_401_es_json(self, client):
        """Verifica que errores 401 retornan JSON."""
        response = client.get('/api/alumnos')
        
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert 'error' in data or 'codigo' in data


# ===========================================================================
# Ejecucion directa (para debug)
# ===========================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
