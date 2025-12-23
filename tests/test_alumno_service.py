# ===========================================================================
# Tests del Servicio de Alumnos
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Fase: 5 - Testing Formal
# ===========================================================================
#
# REGLAS DE TESTING:
# - Usa MockAlumnoRepository (sin BD real)
# - Tests independientes entre si
# - Cada test crea su propio mock
#
# ===========================================================================

"""
Tests unitarios para el servicio de aplicacion AlumnoService.

Usa repositorio mock para aislar la logica de negocio.
"""

import pytest
from datetime import datetime, timezone

# Configuracion de path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from domain.entities.alumno import Alumno
from domain.repositories.alumno_repository import MockAlumnoRepository
from domain.exceptions import ValidacionError, AlumnoNoEncontrado, DNIDuplicado
from application.alumno_service import AlumnoService


@pytest.fixture
def mock_repository():
    """Fixture que crea un repositorio mock limpio para cada test."""
    return MockAlumnoRepository()


@pytest.fixture
def service(mock_repository):
    """Fixture que crea un servicio con el mock repository."""
    return AlumnoService(mock_repository)


class TestCrearAlumno:
    """Tests del caso de uso: Crear Alumno."""
    
    def test_crear_alumno_exitoso(self, service):
        """Verifica que se puede crear un alumno con datos validos."""
        # Act
        alumno = service.crear_alumno(
            nombre="Juan",
            apellido="Perez",
            dni="12345678"
        )
        
        # Assert
        assert alumno.id is not None
        assert alumno.nombre == "Juan"
        assert alumno.apellido == "Perez"
        assert alumno.dni == "12345678"
    
    def test_crear_alumno_aparece_en_lista(self, service):
        """Verifica que el alumno creado aparece en la lista."""
        # Arrange
        service.crear_alumno("Maria", "Garcia", "11111111")
        
        # Act
        lista = service.listar_alumnos()
        
        # Assert
        assert len(lista) == 1
        assert lista[0].nombre == "Maria"
    
    def test_crear_alumno_con_nombre_vacio_falla(self, service):
        """Verifica que crear con nombre vacio lanza ValidacionError."""
        with pytest.raises(ValidacionError) as exc_info:
            service.crear_alumno("", "Perez", "12345678")
        
        assert exc_info.value.campo == "nombre"
    
    def test_crear_alumno_dni_duplicado_falla(self, service):
        """Verifica que DNI duplicado lanza DNIDuplicado."""
        # Arrange: crear primer alumno
        service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act & Assert: intentar crear con mismo DNI
        with pytest.raises(DNIDuplicado):
            service.crear_alumno("Maria", "Garcia", "12345678")


class TestObtenerAlumno:
    """Tests del caso de uso: Obtener Alumno por ID."""
    
    def test_obtener_alumno_existente(self, service):
        """Verifica que se puede obtener un alumno por ID."""
        # Arrange
        creado = service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act
        obtenido = service.obtener_alumno(creado.id)
        
        # Assert
        assert obtenido.id == creado.id
        assert obtenido.nombre == "Juan"
    
    def test_obtener_alumno_inexistente_falla(self, service):
        """Verifica que obtener ID inexistente lanza AlumnoNoEncontrado."""
        with pytest.raises(AlumnoNoEncontrado):
            service.obtener_alumno("id-que-no-existe")


class TestListarAlumnos:
    """Tests del caso de uso: Listar Alumnos."""
    
    def test_listar_sin_alumnos_retorna_lista_vacia(self, service):
        """Verifica que listar sin alumnos retorna lista vacia."""
        lista = service.listar_alumnos()
        
        assert lista == []
        assert len(lista) == 0
    
    def test_listar_multiples_alumnos(self, service):
        """Verifica que listar retorna todos los alumnos."""
        # Arrange
        service.crear_alumno("Juan", "Perez", "11111111")
        service.crear_alumno("Maria", "Garcia", "22222222")
        service.crear_alumno("Carlos", "Lopez", "33333333")
        
        # Act
        lista = service.listar_alumnos()
        
        # Assert
        assert len(lista) == 3
    
    def test_listar_ordenado_por_apellido(self, service):
        """Verifica que la lista viene ordenada por apellido."""
        # Arrange (crear en desorden)
        service.crear_alumno("Carlos", "Zapata", "11111111")
        service.crear_alumno("Ana", "Alvarez", "22222222")
        service.crear_alumno("Juan", "Martinez", "33333333")
        
        # Act
        lista = service.listar_alumnos()
        
        # Assert: ordenados alfabeticamente por apellido
        apellidos = [a.apellido for a in lista]
        assert apellidos == sorted(apellidos)


class TestActualizarAlumno:
    """Tests del caso de uso: Actualizar Alumno."""
    
    def test_actualizar_alumno_exitoso(self, service):
        """Verifica que se puede actualizar un alumno existente."""
        # Arrange
        creado = service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act
        actualizado = service.actualizar_alumno(
            id=creado.id,
            nombre="Juan Carlos",
            apellido="Perez",
            dni="12345678"
        )
        
        # Assert
        assert actualizado.nombre == "Juan Carlos"
    
    def test_actualizar_alumno_inexistente_falla(self, service):
        """Verifica que actualizar ID inexistente lanza error."""
        with pytest.raises(AlumnoNoEncontrado):
            service.actualizar_alumno(
                id="id-que-no-existe",
                nombre="Test",
                apellido="Test",
                dni="123"
            )
    
    def test_actualizar_dni_a_duplicado_falla(self, service):
        """Verifica que cambiar DNI a uno existente falla."""
        # Arrange
        alumno1 = service.crear_alumno("Juan", "Perez", "11111111")
        alumno2 = service.crear_alumno("Maria", "Garcia", "22222222")
        
        # Act & Assert
        with pytest.raises(DNIDuplicado):
            service.actualizar_alumno(
                id=alumno1.id,
                nombre="Juan",
                apellido="Perez",
                dni="22222222"  # DNI del otro alumno
            )
    
    def test_actualizar_mantener_mismo_dni_ok(self, service):
        """Verifica que se puede mantener el mismo DNI al actualizar."""
        # Arrange
        creado = service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act (cambiar nombre pero mantener DNI)
        actualizado = service.actualizar_alumno(
            id=creado.id,
            nombre="Juan Carlos",
            apellido="Perez",
            dni="12345678"  # Mismo DNI
        )
        
        # Assert
        assert actualizado.dni == "12345678"
        assert actualizado.nombre == "Juan Carlos"


class TestEliminarAlumno:
    """Tests del caso de uso: Eliminar Alumno."""
    
    def test_eliminar_alumno_existente(self, service):
        """Verifica que se puede eliminar un alumno existente."""
        # Arrange
        creado = service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act
        resultado = service.eliminar_alumno(creado.id)
        
        # Assert
        assert resultado is True
    
    def test_eliminar_alumno_desaparece_de_lista(self, service):
        """Verifica que el alumno eliminado ya no esta en la lista."""
        # Arrange
        creado = service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act
        service.eliminar_alumno(creado.id)
        lista = service.listar_alumnos()
        
        # Assert
        assert len(lista) == 0
    
    def test_eliminar_alumno_inexistente_falla(self, service):
        """Verifica que eliminar ID inexistente lanza error."""
        with pytest.raises(AlumnoNoEncontrado):
            service.eliminar_alumno("id-que-no-existe")


class TestBuscarPorDni:
    """Tests del caso de uso: Buscar por DNI."""
    
    def test_buscar_por_dni_existente(self, service):
        """Verifica que se puede buscar por DNI existente."""
        # Arrange
        service.crear_alumno("Juan", "Perez", "12345678")
        
        # Act
        encontrado = service.buscar_por_dni("12345678")
        
        # Assert
        assert encontrado is not None
        assert encontrado.dni == "12345678"
    
    def test_buscar_por_dni_inexistente_retorna_none(self, service):
        """Verifica que buscar DNI inexistente retorna None."""
        resultado = service.buscar_por_dni("99999999")
        
        assert resultado is None


# ===========================================================================
# Ejecucion directa (para debug)
# ===========================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
