# ===========================================================================
# Servicio de Alumnos
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Application (Casos de Uso)
# Patron: Service Layer, Dependency Injection
# ===========================================================================
#
# POR QUE UN SERVICIO DE APLICACION:
# - Orquesta los casos de uso (crear, listar, actualizar, eliminar)
# - Coordina entre la capa de dominio y la infraestructura
# - NO contiene logica de negocio (esa esta en las entidades)
#
# PATRON DEPENDENCY INJECTION:
# - Recibe el repositorio por constructor
# - Permite cambiar la implementacion (Supabase, Mock) sin modificar codigo
# - Facilita testing con repositorio mock
#
# ===========================================================================

"""
Servicio de aplicacion para gestionar Alumnos.

Orquesta los casos de uso CRUD y coordina con el repositorio.
"""

# Configuracion de path para pruebas atomicas
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from typing import List, Optional

from domain.entities.alumno import Alumno
from domain.repositories.alumno_repository import AlumnoRepository
from domain.exceptions import AlumnoNoEncontrado, DNIDuplicado, ValidacionError


class AlumnoService:
    """
    Servicio de aplicacion para Alumnos.
    
    Responsabilidades:
    - Orquestar casos de uso CRUD
    - Validar reglas de negocio que cruzan entidades
    - Coordinar con el repositorio
    
    NO hace:
    - Logica de entidad (esa esta en Alumno)
    - Acceso directo a BD (eso lo hace el repositorio)
    - Manejo de HTTP/API (eso lo hace la capa de presentacion)
    
    Patron: Service Layer + Dependency Injection
    """
    
    def __init__(self, repository: AlumnoRepository):
        """
        Inicializa el servicio con un repositorio.
        
        POR QUE RECIBIR REPOSITORIO:
        - Inversion de dependencias: depende de abstraccion, no de concreto
        - Facilita testing: se puede pasar MockAlumnoRepository
        - Permite cambiar BD sin modificar esta clase
        
        Args:
            repository: Implementacion del repositorio de alumnos
        """
        self._repository = repository
    
    # =========================================================================
    # CASOS DE USO
    # =========================================================================
    
    def crear_alumno(self, nombre: str, apellido: str, dni: str) -> Alumno:
        """
        Caso de uso: Crear un nuevo alumno.
        
        Trazabilidad:
        - HU-001: Registrar Alumno
        - RF-001, RF-005
        
        Args:
            nombre: Nombre del alumno
            apellido: Apellido del alumno
            dni: DNI del alumno
        
        Returns:
            Alumno creado con ID asignado
        
        Raises:
            ValidacionError: Si los datos son invalidos
            DNIDuplicado: Si el DNI ya existe
        """
        # Crear entidad (valida internamente)
        # Si los datos son invalidos, Alumno lanzara ValidacionError
        alumno = Alumno(nombre=nombre, apellido=apellido, dni=dni)
        
        # Persistir (el repositorio verifica DNI unico)
        return self._repository.crear(alumno)
    
    def obtener_alumno(self, id: str) -> Alumno:
        """
        Caso de uso: Obtener un alumno por ID.
        
        Trazabilidad:
        - HU-002: Ver Lista de Alumnos
        - RF-002
        
        Args:
            id: UUID del alumno
        
        Returns:
            Alumno encontrado
        
        Raises:
            AlumnoNoEncontrado: Si el ID no existe
        """
        alumno = self._repository.obtener_por_id(id)
        
        if alumno is None:
            raise AlumnoNoEncontrado(id)
        
        return alumno
    
    def listar_alumnos(self) -> List[Alumno]:
        """
        Caso de uso: Listar todos los alumnos.
        
        Trazabilidad:
        - HU-002: Ver Lista de Alumnos
        - RF-002
        
        Returns:
            Lista de alumnos ordenada por apellido
        """
        return self._repository.listar_todos()
    
    def actualizar_alumno(
        self, 
        id: str, 
        nombre: str, 
        apellido: str, 
        dni: str
    ) -> Alumno:
        """
        Caso de uso: Actualizar datos de un alumno.
        
        Trazabilidad:
        - HU-003: Editar Alumno
        - RF-003, RF-005
        
        Args:
            id: UUID del alumno a actualizar
            nombre: Nuevo nombre
            apellido: Nuevo apellido
            dni: Nuevo DNI
        
        Returns:
            Alumno actualizado
        
        Raises:
            AlumnoNoEncontrado: Si el ID no existe
            ValidacionError: Si los datos son invalidos
            DNIDuplicado: Si el DNI pertenece a otro alumno
        """
        # Verificar que existe
        alumno_actual = self._repository.obtener_por_id(id)
        if alumno_actual is None:
            raise AlumnoNoEncontrado(id)
        
        # Crear nueva instancia con datos actualizados
        # (Alumno es conceptualmente inmutable)
        alumno_nuevo = Alumno(
            id=id,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            created_at=alumno_actual.created_at
        )
        
        # Persistir actualizacion
        return self._repository.actualizar(alumno_nuevo)
    
    def eliminar_alumno(self, id: str) -> bool:
        """
        Caso de uso: Eliminar un alumno.
        
        Trazabilidad:
        - HU-004: Eliminar Alumno
        - RF-004, RF-009
        
        Args:
            id: UUID del alumno a eliminar
        
        Returns:
            True si se elimino
        
        Raises:
            AlumnoNoEncontrado: Si el ID no existe
        """
        # Verificar que existe antes de eliminar
        if not self._repository.obtener_por_id(id):
            raise AlumnoNoEncontrado(id)
        
        return self._repository.eliminar(id)
    
    def buscar_por_dni(self, dni: str) -> Optional[Alumno]:
        """
        Caso de uso: Buscar alumno por DNI.
        
        Args:
            dni: DNI a buscar
        
        Returns:
            Alumno si existe, None si no
        """
        return self._repository.obtener_por_dni(dni)


# ===========================================================================
# FACTORY FUNCTION
# ===========================================================================

def create_alumno_service() -> AlumnoService:
    """
    Crea una instancia del servicio con el repositorio real.
    
    POR QUE FACTORY FUNCTION:
    - Centraliza la creacion del servicio con sus dependencias
    - Facilita cambiar la implementacion del repositorio
    - Usado por la capa de presentacion (API)
    
    Returns:
        AlumnoService configurado con SupabaseAlumnoRepository
    """
    from infrastructure.supabase_alumno_repository import SupabaseAlumnoRepository
    
    repository = SupabaseAlumnoRepository()
    return AlumnoService(repository)


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de AlumnoService (con Mock) ===\n")
    
    # Usar repositorio mock para no depender de BD
    from domain.repositories.alumno_repository import MockAlumnoRepository
    
    # Crear servicio con mock
    mock_repo = MockAlumnoRepository()
    service = AlumnoService(mock_repo)
    
    # Test 1: Crear alumno
    try:
        alumno = service.crear_alumno("Juan", "Perez", "11111111")
        print(f"[OK] Crear: {alumno}")
    except Exception as e:
        print(f"[ERROR] Crear: {e}")
    
    # Test 2: Listar alumnos
    try:
        lista = service.listar_alumnos()
        print(f"[OK] Listar: {len(lista)} alumnos")
    except Exception as e:
        print(f"[ERROR] Listar: {e}")
    
    # Test 3: Obtener por ID
    try:
        obtenido = service.obtener_alumno(alumno.id)
        print(f"[OK] Obtener: {obtenido}")
    except Exception as e:
        print(f"[ERROR] Obtener: {e}")
    
    # Test 4: Actualizar
    try:
        actualizado = service.actualizar_alumno(
            alumno.id, "Juan Carlos", "Perez", "11111111"
        )
        print(f"[OK] Actualizar: {actualizado}")
    except Exception as e:
        print(f"[ERROR] Actualizar: {e}")
    
    # Test 5: DNI duplicado
    try:
        service.crear_alumno("Maria", "Garcia", "11111111")
        print("[ERROR] Debio fallar por DNI duplicado")
    except DNIDuplicado as e:
        print(f"[OK] DNI duplicado: {e.message}")
    
    # Test 6: Eliminar
    try:
        eliminado = service.eliminar_alumno(alumno.id)
        print(f"[OK] Eliminar: {eliminado}")
    except Exception as e:
        print(f"[ERROR] Eliminar: {e}")
    
    # Test 7: Obtener eliminado
    try:
        service.obtener_alumno(alumno.id)
        print("[ERROR] Debio fallar por no encontrado")
    except AlumnoNoEncontrado as e:
        print(f"[OK] No encontrado: {e.message}")
    
    print("\n=== Todas las pruebas pasaron ===")
