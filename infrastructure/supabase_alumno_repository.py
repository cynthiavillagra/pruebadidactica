# ===========================================================================
# Repositorio Supabase de Alumnos
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Infrastructure
# Patron: Repository (Implementacion), Adapter
# ===========================================================================
#
# POR QUE IMPLEMENTACION SEPARADA:
# - La interface (AlumnoRepository) esta en domain
# - Esta clase implementa la interface usando Supabase
# - Podemos cambiar a otra BD sin tocar el dominio ni el servicio
#
# PATRON ADAPTER:
# - Traduce las respuestas de Supabase a nuestras entidades de dominio
# - Aísla la dependencia de Supabase en esta clase
#
# ===========================================================================

"""
Implementacion del repositorio de Alumnos usando Supabase.

Traduce las operaciones CRUD a llamadas a la API de Supabase.
"""

# Configuracion de path para pruebas atomicas
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from typing import Optional, List

from domain.entities.alumno import Alumno
from domain.repositories.alumno_repository import AlumnoRepository
from domain.exceptions import (
    AlumnoNoEncontrado,
    DNIDuplicado,
    RepositoryError
)
from infrastructure.supabase_client import get_supabase_client


class SupabaseAlumnoRepository(AlumnoRepository):
    """
    Implementacion del repositorio de Alumnos usando Supabase.
    
    Esta clase:
    - Implementa la interface AlumnoRepository
    - Usa el cliente Supabase singleton
    - Traduce entre dict de Supabase y entidades de dominio
    
    Patron: Repository + Adapter
    """
    
    # Nombre de la tabla en Supabase
    TABLE_NAME = 'alumnos'
    
    def __init__(self):
        """
        Inicializa el repositorio.
        
        POR QUE NO RECIBE CLIENTE:
        - Usa el singleton para garantizar una sola conexion
        - El cliente se obtiene lazy (solo cuando se necesita)
        """
        self._client = None
    
    @property
    def client(self):
        """
        Obtiene el cliente Supabase (lazy loading).
        
        POR QUE PROPERTY:
        - Permite obtener el cliente solo cuando se necesita
        - Facilita testing (se puede mockear)
        """
        if self._client is None:
            self._client = get_supabase_client()
        return self._client
    
    @property
    def table(self):
        """Acceso directo a la tabla de alumnos."""
        return self.client.table(self.TABLE_NAME)
    
    # =========================================================================
    # METODOS CRUD (Implementacion de la interface)
    # =========================================================================
    
    def crear(self, alumno: Alumno) -> Alumno:
        """
        Crea un nuevo alumno en Supabase.
        
        Args:
            alumno: Entidad Alumno a persistir
        
        Returns:
            Alumno con ID asignado
        
        Raises:
            DNIDuplicado: Si el DNI ya existe
            RepositoryError: Si hay error de BD
        """
        try:
            # Verificar DNI unico antes de insertar
            if self.existe_dni(alumno.dni):
                raise DNIDuplicado(alumno.dni)
            
            # Preparar datos para insertar
            data = {
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'dni': alumno.dni
            }
            
            # Insertar y obtener el registro creado
            response = self.table.insert(data).execute()
            
            if not response.data:
                raise RepositoryError("No se pudo crear el alumno")
            
            # Convertir respuesta a entidad
            return self._map_to_entity(response.data[0])
            
        except DNIDuplicado:
            raise
        except Exception as e:
            # Detectar error de constraint de unicidad
            if 'duplicate key' in str(e).lower() or 'unique' in str(e).lower():
                raise DNIDuplicado(alumno.dni)
            raise RepositoryError(f"Error al crear alumno: {e}")
    
    def obtener_por_id(self, id: str) -> Optional[Alumno]:
        """
        Busca un alumno por su ID.
        
        Args:
            id: UUID del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        try:
            response = self.table.select('*').eq('id', id).execute()
            
            if not response.data:
                return None
            
            return self._map_to_entity(response.data[0])
            
        except Exception as e:
            raise RepositoryError(f"Error al buscar alumno: {e}")
    
    def obtener_por_dni(self, dni: str) -> Optional[Alumno]:
        """
        Busca un alumno por su DNI.
        
        Args:
            dni: DNI del alumno
        
        Returns:
            Alumno si existe, None si no
        """
        try:
            response = self.table.select('*').eq('dni', dni.upper()).execute()
            
            if not response.data:
                return None
            
            return self._map_to_entity(response.data[0])
            
        except Exception as e:
            raise RepositoryError(f"Error al buscar por DNI: {e}")
    
    def listar_todos(self) -> List[Alumno]:
        """
        Obtiene todos los alumnos ordenados por apellido.
        
        Returns:
            Lista de alumnos
        """
        try:
            response = self.table.select('*').order('apellido').execute()
            
            return [self._map_to_entity(data) for data in response.data]
            
        except Exception as e:
            raise RepositoryError(f"Error al listar alumnos: {e}")
    
    def actualizar(self, alumno: Alumno) -> Alumno:
        """
        Actualiza un alumno existente.
        
        Args:
            alumno: Entidad Alumno con los nuevos datos
        
        Returns:
            Alumno actualizado
        
        Raises:
            AlumnoNoEncontrado: Si el ID no existe
            DNIDuplicado: Si el nuevo DNI pertenece a otro alumno
        """
        try:
            # Verificar que existe
            if not self.obtener_por_id(alumno.id):
                raise AlumnoNoEncontrado(alumno.id)
            
            # Verificar DNI unico (excluyendo el actual)
            if self.existe_dni(alumno.dni, excluir_id=alumno.id):
                raise DNIDuplicado(alumno.dni)
            
            # Preparar datos para actualizar
            data = {
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'dni': alumno.dni
            }
            
            # Actualizar
            response = self.table.update(data).eq('id', alumno.id).execute()
            
            if not response.data:
                raise RepositoryError("No se pudo actualizar el alumno")
            
            return self._map_to_entity(response.data[0])
            
        except (AlumnoNoEncontrado, DNIDuplicado):
            raise
        except Exception as e:
            if 'duplicate key' in str(e).lower() or 'unique' in str(e).lower():
                raise DNIDuplicado(alumno.dni)
            raise RepositoryError(f"Error al actualizar alumno: {e}")
    
    def eliminar(self, id: str) -> bool:
        """
        Elimina un alumno por su ID.
        
        Args:
            id: UUID del alumno
        
        Returns:
            True si se elimino, False si no existia
        """
        try:
            # Verificar que existe antes de eliminar
            if not self.obtener_por_id(id):
                return False
            
            self.table.delete().eq('id', id).execute()
            return True
            
        except Exception as e:
            raise RepositoryError(f"Error al eliminar alumno: {e}")
    
    def existe_dni(self, dni: str, excluir_id: Optional[str] = None) -> bool:
        """
        Verifica si un DNI ya existe.
        
        Args:
            dni: DNI a verificar
            excluir_id: ID a excluir de la busqueda
        
        Returns:
            True si el DNI existe (y no es del alumno excluido)
        """
        try:
            query = self.table.select('id').eq('dni', dni.upper())
            
            if excluir_id:
                query = query.neq('id', excluir_id)
            
            response = query.execute()
            
            return len(response.data) > 0
            
        except Exception as e:
            raise RepositoryError(f"Error al verificar DNI: {e}")
    
    # =========================================================================
    # METODOS PRIVADOS (Adapter)
    # =========================================================================
    
    def _map_to_entity(self, data: dict) -> Alumno:
        """
        Convierte un dict de Supabase a entidad Alumno.
        
        POR QUE METODO SEPARADO (ADAPTER):
        - Centraliza la conversion
        - Si Supabase cambia formato, solo se modifica aqui
        """
        return Alumno.from_dict(data)


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de SupabaseAlumnoRepository ===\n")
    
    try:
        # Crear repositorio
        repo = SupabaseAlumnoRepository()
        print("[OK] Repositorio creado")
        
        # Intentar listar (verifica conexion)
        alumnos = repo.listar_todos()
        print(f"[OK] Listar alumnos: {len(alumnos)} encontrados")
        
        for alumno in alumnos[:3]:  # Mostrar max 3
            print(f"     - {alumno}")
        
        print("\n=== Prueba pasada ===")
        
    except EnvironmentError as e:
        print(f"[ADVERTENCIA] {e}")
        print("\nEsto es esperado si no tienes .env configurado.")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nVerifica:")
        print("  1. El archivo .env tiene las credenciales correctas")
        print("  2. La tabla 'alumnos' existe en Supabase")
        print("  3. Las politicas RLS estan configuradas")
