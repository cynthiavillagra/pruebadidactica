# domain/repositories/__init__.py
from domain.repositories.alumno_repository import AlumnoRepository, MockAlumnoRepository

__all__ = ['AlumnoRepository', 'MockAlumnoRepository']
