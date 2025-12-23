# ===========================================================================
# Tests de la Entidad Alumno
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Fase: 5 - Testing Formal
# ===========================================================================
#
# REGLAS DE TESTING:
# - Sin credenciales reales (no se conecta a Supabase)
# - Fechas con timezone.utc
# - Tests independientes entre si
#
# ===========================================================================

"""
Tests unitarios para la entidad Alumno.

Valida las reglas de negocio de la entidad de dominio.
"""

import pytest
from datetime import datetime, timezone

# Configuracion de path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from domain.entities.alumno import Alumno
from domain.exceptions import ValidacionError


class TestAlumnoCreacion:
    """Tests de creacion de Alumno."""
    
    def test_crear_alumno_valido(self):
        """Verifica que se puede crear un alumno con datos validos."""
        # Arrange & Act
        alumno = Alumno(nombre="Juan", apellido="Perez", dni="12345678")
        
        # Assert
        assert alumno.nombre == "Juan"
        assert alumno.apellido == "Perez"
        assert alumno.dni == "12345678"
        assert alumno.es_nuevo() is True
    
    def test_nombre_se_normaliza_title_case(self):
        """Verifica que el nombre se convierte a Title Case."""
        alumno = Alumno(nombre="maria", apellido="garcia", dni="11111111")
        
        assert alumno.nombre == "Maria"
        assert alumno.apellido == "Garcia"
    
    def test_dni_se_normaliza_mayusculas(self):
        """Verifica que el DNI se convierte a mayusculas."""
        alumno = Alumno(nombre="Test", apellido="Test", dni="abc123")
        
        assert alumno.dni == "ABC123"
    
    def test_espacios_se_eliminan(self):
        """Verifica que se eliminan espacios al inicio y final."""
        alumno = Alumno(nombre="  Juan  ", apellido="  Perez  ", dni="  123  ")
        
        assert alumno.nombre == "Juan"
        assert alumno.apellido == "Perez"
        assert alumno.dni == "123"


class TestAlumnoValidacion:
    """Tests de validacion de datos."""
    
    def test_nombre_vacio_lanza_error(self):
        """Verifica que nombre vacio lanza ValidacionError."""
        with pytest.raises(ValidacionError) as exc_info:
            Alumno(nombre="", apellido="Perez", dni="12345678")
        
        assert exc_info.value.campo == "nombre"
        assert "requerido" in exc_info.value.message.lower()
    
    def test_nombre_solo_espacios_lanza_error(self):
        """Verifica que nombre con solo espacios lanza error."""
        with pytest.raises(ValidacionError):
            Alumno(nombre="   ", apellido="Perez", dni="12345678")
    
    def test_apellido_vacio_lanza_error(self):
        """Verifica que apellido vacio lanza ValidacionError."""
        with pytest.raises(ValidacionError) as exc_info:
            Alumno(nombre="Juan", apellido="", dni="12345678")
        
        assert exc_info.value.campo == "apellido"
    
    def test_dni_vacio_lanza_error(self):
        """Verifica que DNI vacio lanza ValidacionError."""
        with pytest.raises(ValidacionError) as exc_info:
            Alumno(nombre="Juan", apellido="Perez", dni="")
        
        assert exc_info.value.campo == "dni"
    
    def test_nombre_muy_largo_lanza_error(self):
        """Verifica que nombre > 100 caracteres lanza error."""
        nombre_largo = "A" * 101
        
        with pytest.raises(ValidacionError) as exc_info:
            Alumno(nombre=nombre_largo, apellido="Perez", dni="123")
        
        assert exc_info.value.campo == "nombre"
        assert "100" in exc_info.value.message


class TestAlumnoFechas:
    """Tests de manejo de fechas."""
    
    def test_created_at_se_genera_automaticamente(self):
        """Verifica que created_at se genera al crear."""
        antes = datetime.now(timezone.utc)
        alumno = Alumno(nombre="Test", apellido="Test", dni="123")
        despues = datetime.now(timezone.utc)
        
        assert alumno.created_at is not None
        assert antes <= alumno.created_at <= despues
    
    def test_updated_at_se_genera_automaticamente(self):
        """Verifica que updated_at se genera al crear."""
        alumno = Alumno(nombre="Test", apellido="Test", dni="123")
        
        assert alumno.updated_at is not None
    
    def test_fechas_son_utc(self):
        """Verifica que las fechas estan en UTC."""
        alumno = Alumno(nombre="Test", apellido="Test", dni="123")
        
        assert alumno.created_at.tzinfo is not None


class TestAlumnoFactoryMethods:
    """Tests de metodos factory."""
    
    def test_from_dict_crea_alumno(self):
        """Verifica que from_dict crea un alumno desde diccionario."""
        data = {
            'id': 'abc-123',
            'nombre': 'Maria',
            'apellido': 'Garcia',
            'dni': '87654321'
        }
        
        alumno = Alumno.from_dict(data)
        
        assert alumno.id == 'abc-123'
        assert alumno.nombre == 'Maria'
        assert alumno.dni == '87654321'
    
    def test_from_dict_parsea_fechas_iso(self):
        """Verifica que from_dict parsea fechas ISO8601."""
        data = {
            'nombre': 'Test',
            'apellido': 'Test',
            'dni': '123',
            'created_at': '2025-01-01T10:00:00+00:00'
        }
        
        alumno = Alumno.from_dict(data)
        
        assert alumno.created_at.year == 2025
        assert alumno.created_at.month == 1
    
    def test_to_dict_retorna_diccionario(self):
        """Verifica que to_dict retorna un diccionario completo."""
        alumno = Alumno(
            id='test-id',
            nombre='Juan',
            apellido='Perez',
            dni='12345678'
        )
        
        result = alumno.to_dict()
        
        assert result['id'] == 'test-id'
        assert result['nombre'] == 'Juan'
        assert result['apellido'] == 'Perez'
        assert result['dni'] == '12345678'
        assert 'created_at' in result
        assert 'updated_at' in result


class TestAlumnoActualizar:
    """Tests del metodo actualizar."""
    
    def test_actualizar_crea_nueva_instancia(self):
        """Verifica que actualizar retorna nueva instancia."""
        original = Alumno(nombre="Juan", apellido="Perez", dni="123")
        actualizado = original.actualizar(nombre="Juan Carlos")
        
        # Son instancias diferentes
        assert original is not actualizado
        
        # Original no cambio
        assert original.nombre == "Juan"
        
        # Nuevo tiene el cambio
        assert actualizado.nombre == "Juan Carlos"
    
    def test_actualizar_mantiene_datos_no_modificados(self):
        """Verifica que los datos no especificados se mantienen."""
        original = Alumno(
            id='test-id',
            nombre="Juan",
            apellido="Perez",
            dni="123"
        )
        
        actualizado = original.actualizar(nombre="Maria")
        
        assert actualizado.id == 'test-id'
        assert actualizado.apellido == "Perez"
        assert actualizado.dni == "123"


class TestAlumnoEquality:
    """Tests de igualdad y hash."""
    
    def test_alumnos_con_mismo_id_son_iguales(self):
        """Verifica que dos alumnos con mismo ID son iguales."""
        alumno1 = Alumno(id='123', nombre="Juan", apellido="Perez", dni="111")
        alumno2 = Alumno(id='123', nombre="Maria", apellido="Garcia", dni="222")
        
        assert alumno1 == alumno2
    
    def test_alumnos_con_diferente_id_no_son_iguales(self):
        """Verifica que alumnos con diferente ID son diferentes."""
        alumno1 = Alumno(id='123', nombre="Juan", apellido="Perez", dni="111")
        alumno2 = Alumno(id='456', nombre="Juan", apellido="Perez", dni="111")
        
        assert alumno1 != alumno2
    
    def test_nombre_completo(self):
        """Verifica la propiedad nombre_completo."""
        alumno = Alumno(nombre="Juan", apellido="Perez", dni="123")
        
        assert alumno.nombre_completo == "Juan Perez"


# ===========================================================================
# Ejecucion directa (para debug)
# ===========================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
