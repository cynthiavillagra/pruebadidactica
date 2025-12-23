# ===========================================================================
# Entidad Alumno
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Domain (Nucleo)
# Trazabilidad: RF-001, RF-002, RF-003, RF-004, RF-005
# ===========================================================================
#
# POR QUE ENTIDAD EN CAPA DE DOMINIO:
# - Representa el concepto de negocio "Alumno"
# - Contiene reglas de validacion propias
# - NO conoce Flask, Supabase ni ninguna tecnologia externa
# - Es el nucleo de la aplicacion, todo lo demas depende de ella
#
# ===========================================================================

"""
Entidad de dominio: Alumno

Esta clase representa un alumno con sus reglas de negocio.
Es independiente de frameworks y bases de datos.
"""

# Configuracion de path para pruebas atomicas
# POR QUE: Permite ejecutar el archivo directamente con python domain/entities/alumno.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from datetime import datetime, timezone
from typing import Optional
from domain.exceptions import ValidacionError


class Alumno:
    """
    Entidad que representa un Alumno en el sistema.
    
    Atributos:
        id: Identificador unico (UUID como string)
        nombre: Nombre del alumno (1-100 caracteres)
        apellido: Apellido del alumno (1-100 caracteres)
        dni: Documento Nacional de Identidad (unico, 1-20 caracteres)
        created_at: Fecha de creacion (UTC)
        updated_at: Fecha de ultima modificacion (UTC)
    
    Patrones aplicados:
        - Factory Method: from_dict() para crear desde diccionario
        - Value Object: Inmutabilidad conceptual (atributos privados)
    """
    
    # Constantes de validacion
    NOMBRE_MAX_LENGTH = 100
    APELLIDO_MAX_LENGTH = 100
    DNI_MAX_LENGTH = 20
    
    def __init__(
        self,
        nombre: str,
        apellido: str,
        dni: str,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa un alumno con validaciones.
        
        POR QUE VALIDAR EN CONSTRUCTOR:
        - Garantiza que nunca exista un Alumno invalido
        - Fail-fast: errores se detectan al crear, no al usar
        
        Args:
            nombre: Nombre del alumno
            apellido: Apellido del alumno
            dni: DNI del alumno
            id: ID opcional (se genera al persistir)
            created_at: Fecha de creacion opcional
            updated_at: Fecha de modificacion opcional
        
        Raises:
            ValidacionError: Si los datos no cumplen las reglas
        """
        # Validar ANTES de asignar (fail-fast)
        self._validar_nombre(nombre)
        self._validar_apellido(apellido)
        self._validar_dni(dni)
        
        # Asignar atributos (normalizados)
        self._id = id
        self._nombre = nombre.strip().title()  # "juan" -> "Juan"
        self._apellido = apellido.strip().title()
        self._dni = dni.strip().upper()  # Normalizar a mayusculas
        self._created_at = created_at or datetime.now(timezone.utc)
        self._updated_at = updated_at or datetime.now(timezone.utc)
    
    # =========================================================================
    # PROPERTIES (Getters - Encapsulacion)
    # =========================================================================
    
    @property
    def id(self) -> Optional[str]:
        """Retorna el ID del alumno."""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre del alumno."""
        return self._nombre
    
    @property
    def apellido(self) -> str:
        """Retorna el apellido del alumno."""
        return self._apellido
    
    @property
    def dni(self) -> str:
        """Retorna el DNI del alumno."""
        return self._dni
    
    @property
    def created_at(self) -> datetime:
        """Retorna la fecha de creacion."""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """Retorna la fecha de ultima modificacion."""
        return self._updated_at
    
    @property
    def nombre_completo(self) -> str:
        """Retorna nombre y apellido concatenados."""
        return f"{self._nombre} {self._apellido}"
    
    # =========================================================================
    # FACTORY METHODS
    # =========================================================================
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Alumno':
        """
        Crea un Alumno desde un diccionario.
        
        POR QUE FACTORY METHOD:
        - Centraliza la conversion dict -> Alumno
        - Maneja campos opcionales de forma consistente
        - Facilita la integracion con APIs y bases de datos
        
        Args:
            data: Diccionario con los datos del alumno
        
        Returns:
            Instancia de Alumno
        
        Raises:
            ValidacionError: Si los datos son invalidos
        """
        # Parsear fechas si vienen como string (ISO8601)
        created_at = data.get('created_at')
        updated_at = data.get('updated_at')
        
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            apellido=data.get('apellido', ''),
            dni=data.get('dni', ''),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self) -> dict:
        """
        Convierte el Alumno a diccionario.
        
        POR QUE TO_DICT:
        - Facilita serializacion a JSON
        - Desacopla la entidad del formato de transporte
        
        Returns:
            Diccionario con los datos del alumno
        """
        return {
            'id': self._id,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'dni': self._dni,
            'created_at': self._created_at.isoformat() if self._created_at else None,
            'updated_at': self._updated_at.isoformat() if self._updated_at else None
        }
    
    # =========================================================================
    # METODOS DE VALIDACION (Privados)
    # =========================================================================
    
    def _validar_nombre(self, nombre: str) -> None:
        """Valida el campo nombre."""
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre es requerido", campo="nombre")
        
        if len(nombre.strip()) > self.NOMBRE_MAX_LENGTH:
            raise ValidacionError(
                f"El nombre no puede tener mas de {self.NOMBRE_MAX_LENGTH} caracteres",
                campo="nombre"
            )
    
    def _validar_apellido(self, apellido: str) -> None:
        """Valida el campo apellido."""
        if not apellido or not apellido.strip():
            raise ValidacionError("El apellido es requerido", campo="apellido")
        
        if len(apellido.strip()) > self.APELLIDO_MAX_LENGTH:
            raise ValidacionError(
                f"El apellido no puede tener mas de {self.APELLIDO_MAX_LENGTH} caracteres",
                campo="apellido"
            )
    
    def _validar_dni(self, dni: str) -> None:
        """
        Valida el campo DNI.
        
        POR QUE NO VALIDAR FORMATO ESPECIFICO:
        - Diferentes paises tienen formatos distintos
        - Argentina: 8 digitos, Espana: 8 digitos + letra
        - Solo validamos presencia y longitud maxima
        """
        if not dni or not dni.strip():
            raise ValidacionError("El DNI es requerido", campo="dni")
        
        if len(dni.strip()) > self.DNI_MAX_LENGTH:
            raise ValidacionError(
                f"El DNI no puede tener mas de {self.DNI_MAX_LENGTH} caracteres",
                campo="dni"
            )
    
    # =========================================================================
    # METODOS DE DOMINIO
    # =========================================================================
    
    def es_nuevo(self) -> bool:
        """
        Indica si el alumno es nuevo (no persistido).
        
        Returns:
            True si no tiene ID asignado
        """
        return self._id is None
    
    def actualizar(self, nombre: str = None, apellido: str = None, dni: str = None) -> 'Alumno':
        """
        Crea una nueva instancia con los datos actualizados.
        
        POR QUE RETORNAR NUEVA INSTANCIA:
        - Inmutabilidad: no modificamos el objeto original
        - Facilita testing y debugging
        
        Args:
            nombre: Nuevo nombre (opcional)
            apellido: Nuevo apellido (opcional)
            dni: Nuevo DNI (opcional)
        
        Returns:
            Nueva instancia de Alumno con los datos actualizados
        """
        return Alumno(
            id=self._id,
            nombre=nombre if nombre is not None else self._nombre,
            apellido=apellido if apellido is not None else self._apellido,
            dni=dni if dni is not None else self._dni,
            created_at=self._created_at,
            updated_at=datetime.now(timezone.utc)  # Actualizar timestamp
        )
    
    # =========================================================================
    # METODOS ESPECIALES
    # =========================================================================
    
    def __eq__(self, other) -> bool:
        """Dos alumnos son iguales si tienen el mismo ID."""
        if not isinstance(other, Alumno):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash basado en ID para uso en sets/dicts."""
        return hash(self._id)
    
    def __repr__(self) -> str:
        """Representacion para debugging."""
        return f"Alumno(id={self._id}, nombre='{self._nombre}', apellido='{self._apellido}', dni='{self._dni}')"
    
    def __str__(self) -> str:
        """Representacion legible."""
        return f"{self.nombre_completo} (DNI: {self._dni})"


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Entidad Alumno ===\n")
    
    # Test 1: Creacion valida
    try:
        alumno = Alumno(nombre="Juan", apellido="Perez", dni="12345678")
        print(f"[OK] Creacion: {alumno}")
        print(f"     - Nombre normalizado: {alumno.nombre}")
        print(f"     - Es nuevo: {alumno.es_nuevo()}")
    except Exception as e:
        print(f"[ERROR] Creacion: {e}")
    
    # Test 2: Nombre vacio (debe fallar)
    try:
        alumno_malo = Alumno(nombre="", apellido="Test", dni="111")
        print("[ERROR] Debio fallar con nombre vacio")
    except ValidacionError as e:
        print(f"[OK] Validacion nombre: {e.message}")
    
    # Test 3: from_dict
    try:
        data = {"id": "abc-123", "nombre": "maria", "apellido": "garcia", "dni": "87654321"}
        alumno2 = Alumno.from_dict(data)
        print(f"[OK] from_dict: {alumno2}")
    except Exception as e:
        print(f"[ERROR] from_dict: {e}")
    
    # Test 4: to_dict
    try:
        dict_alumno = alumno2.to_dict()
        print(f"[OK] to_dict: {dict_alumno}")
    except Exception as e:
        print(f"[ERROR] to_dict: {e}")
    
    # Test 5: actualizar (inmutable)
    try:
        alumno_actualizado = alumno.actualizar(nombre="Juan Carlos")
        print(f"[OK] Actualizar: {alumno_actualizado}")
        print(f"     - Original sin cambios: {alumno}")
    except Exception as e:
        print(f"[ERROR] actualizar: {e}")
    
    print("\n=== Todas las pruebas pasaron ===")
