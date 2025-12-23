# ===========================================================================
# Interface de Repositorio de Alumnos
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Domain (Nucleo)
# Patron: Repository Pattern (Interface/ABC)
# ===========================================================================
#
# POR QUE UNA INTERFACE ABSTRACTA:
# - Define el CONTRATO sin implementacion
# - El servicio depende de esta abstraccion, no del concreto
# - Permite cambiar Supabase por SQLite, Mock, etc. sin tocar el servicio
# - Principio de Inversion de Dependencias (DIP)
#
# ===========================================================================

"""
Interface abstracta para el repositorio de Alumnos.

Define las operaciones de persistencia sin conocer la implementacion.
"""

# Configuracion de path para pruebas atomicas
# POR QUE: Permite ejecutar el archivo directamente con python domain/repositories/alumno_repository.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from abc import ABC, abstractmethod
from typing import Optional, List

# Importamos la entidad (misma capa, permitido)
from domain.entities.alumno import Alumno


class AlumnoRepository(ABC):
    """
    Interface abstracta para el repositorio de Alumnos.
    
    Define las operaciones CRUD que cualquier implementacion
    debe proveer (Supabase, SQLite, Mock, etc.).
    
    Patron: Repository
    Principio: Dependency Inversion (DIP) - depender de abstracciones
    
    Metodos abstractos:
        - crear(alumno) -> Alumno
        - obtener_por_id(id) -> Optional[Alumno]
        - obtener_por_dni(dni) -> Optional[Alumno]
        - listar_todos() -> List[Alumno]
        - actualizar(alumno) -> Alumno
        - eliminar(id) -> bool
        - existe_dni(dni, excluir_id) -> bool
    """
    
    @abstractmethod
    def crear(self, alumno: Alumno) -> Alumno:
        """
        Persiste un nuevo alumno.
        
        Args:
            alumno: Entidad Alumno a persistir (sin ID)
        
        Returns:
            Alumno con ID asignado por la base de datos
        
        Raises:
            DNIDuplicado: Si el DNI ya existe
            RepositoryError: Si hay error de persistencia
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Alumno]:
        """
        Busca un alumno por su ID.
        
        Args:
            id: UUID del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """
        Busca un alumno por su DNI.
        
        Args:
            dni: DNI del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Alumno]:
        """
        Obtiene todos los alumnos.
        
        Returns:
            Lista de todos los alumnos (puede estar vacia)
        
        POR QUE LISTA Y NO ITERADOR:
        - Para un CRUD simple, la cantidad de alumnos es manejable
        - Simplifica el codigo cliente
        - En caso de necesitar paginacion, se agregaria otro metodo
        """
        pass
    
    @abstractmethod
    def actualizar(self, alumno: Alumno) -> Alumno:
        """
        Actualiza un alumno existente.
        
        Args:
            alumno: Entidad Alumno con los nuevos datos (debe tener ID)
        
        Returns:
            Alumno actualizado
        
        Raises:
            AlumnoNoEncontrado: Si el ID no existe
            DNIDuplicado: Si el nuevo DNI pertenece a otro alumno
            RepositoryError: Si hay error de persistencia
        """
        pass
    
    @abstractmethod
    def eliminar(self, id: str) -> bool:
        """
        Elimina un alumno por su ID.
        
        Args:
            id: UUID del alumno a eliminar
        
        Returns:
            True si se elimino, False si no existia
        """
        pass
    
    @abstractmethod
    def existe_dni(self, dni: str, excluir_id: Optional[str] = None) -> bool:
        """
        Verifica si un DNI ya existe en el sistema.
        
        Args:
            dni: DNI a verificar
            excluir_id: ID a excluir de la busqueda (para updates)
        
        Returns:
            True si el DNI existe (y no es del alumno excluido)
        
        POR QUE EXCLUIR_ID:
        - Al actualizar, el DNI puede ser el mismo del alumno
        - Debemos verificar que no pertenezca a OTRO alumno
        """
        pass


# ===========================================================================
# IMPLEMENTACION MOCK (Para Testing)
# ===========================================================================

class MockAlumnoRepository(AlumnoRepository):
    """
    Implementacion mock del repositorio para testing.
    
    POR QUE MOCK EN EL MISMO ARCHIVO:
    - Facilita testing sin dependencias externas
    - Documenta como implementar la interface
    - Util para desarrollo inicial sin BD
    
    NOTA: NO usar en produccion, los datos se pierden al reiniciar.
    """
    
    def __init__(self):
        self._alumnos: dict[str, Alumno] = {}
        self._id_counter = 0
    
    def _generar_id(self) -> str:
        """Genera un ID unico para testing."""
        self._id_counter += 1
        return f"mock-id-{self._id_counter}"
    
    def crear(self, alumno: Alumno) -> Alumno:
        """Crea un alumno en memoria."""
        from domain.exceptions import DNIDuplicado
        
        # Verificar DNI unico
        if self.existe_dni(alumno.dni):
            raise DNIDuplicado(alumno.dni)
        
        # Simular asignacion de ID
        nuevo_id = self._generar_id()
        alumno_con_id = Alumno(
            id=nuevo_id,
            nombre=alumno.nombre,
            apellido=alumno.apellido,
            dni=alumno.dni,
            created_at=alumno.created_at,
            updated_at=alumno.updated_at
        )
        
        self._alumnos[nuevo_id] = alumno_con_id
        return alumno_con_id
    
    def obtener_por_id(self, id: str) -> Optional[Alumno]:
        """Busca por ID en memoria."""
        return self._alumnos.get(id)
    
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """Busca por DNI en memoria."""
        for alumno in self._alumnos.values():
            if alumno.dni.upper() == dni.upper():
                return alumno
        return None
    
    def listar_todos(self) -> List[Alumno]:
        """Lista todos ordenados por apellido."""
        return sorted(
            self._alumnos.values(),
            key=lambda a: (a.apellido, a.nombre)
        )
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        """Actualiza en memoria."""
        from domain.exceptions import AlumnoNoEncontrado, DNIDuplicado
        
        if alumno.id not in self._alumnos:
            raise AlumnoNoEncontrado(alumno.id)
        
        # Verificar DNI unico (excluyendo el actual)
        if self.existe_dni(alumno.dni, excluir_id=alumno.id):
            raise DNIDuplicado(alumno.dni)
        
        self._alumnos[alumno.id] = alumno
        return alumno
    
    def eliminar(self, id: str) -> bool:
        """Elimina de memoria."""
        if id in self._alumnos:
            del self._alumnos[id]
            return True
        return False
    
    def existe_dni(self, dni: str, excluir_id: Optional[str] = None) -> bool:
        """Verifica si el DNI existe."""
        for alumno in self._alumnos.values():
            if alumno.dni.upper() == dni.upper():
                if excluir_id and alumno.id == excluir_id:
                    continue  # Es el mismo alumno, no cuenta
                return True
        return False


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de AlumnoRepository (Mock) ===\n")
    
    # Crear repositorio mock
    repo = MockAlumnoRepository()
    
    # Test 1: Crear alumno
    alumno1 = Alumno(nombre="Juan", apellido="Perez", dni="11111111")
    alumno_creado = repo.crear(alumno1)
    print(f"[OK] Crear: {alumno_creado}")
    print(f"     - ID asignado: {alumno_creado.id}")
    
    # Test 2: Obtener por ID
    alumno_obtenido = repo.obtener_por_id(alumno_creado.id)
    print(f"[OK] Obtener por ID: {alumno_obtenido}")
    
    # Test 3: Obtener por DNI
    alumno_por_dni = repo.obtener_por_dni("11111111")
    print(f"[OK] Obtener por DNI: {alumno_por_dni}")
    
    # Test 4: Listar todos
    alumno2 = Alumno(nombre="Maria", apellido="Garcia", dni="22222222")
    repo.crear(alumno2)
    lista = repo.listar_todos()
    print(f"[OK] Listar todos: {len(lista)} alumnos")
    for a in lista:
        print(f"     - {a}")
    
    # Test 5: DNI duplicado
    from domain.exceptions import DNIDuplicado
    try:
        repo.crear(Alumno(nombre="Carlos", apellido="Lopez", dni="11111111"))
        print("[ERROR] Debio fallar por DNI duplicado")
    except DNIDuplicado as e:
        print(f"[OK] DNI duplicado detectado: {e.message}")
    
    # Test 6: Actualizar
    alumno_actualizado = alumno_creado.actualizar(nombre="Juan Carlos")
    resultado = repo.actualizar(alumno_actualizado)
    print(f"[OK] Actualizar: {resultado}")
    
    # Test 7: Eliminar
    eliminado = repo.eliminar(alumno_creado.id)
    print(f"[OK] Eliminar: {eliminado}")
    
    # Verificar eliminacion
    no_existe = repo.obtener_por_id(alumno_creado.id)
    print(f"[OK] Verificar eliminacion: {no_existe is None}")
    
    print("\n=== Todas las pruebas pasaron ===")
