# ===========================================================================
# Cliente Supabase (Singleton)
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Infrastructure
# Patron: Singleton (Thread-Safe)
# ===========================================================================
#
# POR QUE SINGLETON PARA EL CLIENTE:
# - Una sola conexion/pool es mas eficiente
# - Evita crear multiples clientes innecesarios
# - Thread-safe para concurrencia
#
# NOTA STATELESS:
# - Este singleton es SEGURO en serverless porque:
#   - Solo mantiene configuracion de conexion
#   - NO guarda estado de usuario/sesion
#   - Cada request usa el cliente pero no modifica su estado interno
#
# ===========================================================================

"""
Cliente Supabase con patron Singleton.

Proporciona una unica instancia del cliente para toda la aplicacion.
"""

# Configuracion de path para pruebas atomicas
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from threading import Lock
from typing import Optional
from supabase import create_client, Client


# Variables del singleton
_supabase_client: Optional[Client] = None
_lock = Lock()


def get_supabase_client() -> Client:
    """
    Retorna la instancia singleton del cliente Supabase.
    
    POR QUE LAZY INITIALIZATION:
    - El cliente se crea solo cuando se necesita
    - Permite que la app inicie sin conexion a BD (para docs, etc.)
    
    POR QUE DOUBLE-CHECK LOCKING:
    - Thread-safe sin overhead innecesario
    - Solo usa lock cuando es necesario crear el cliente
    
    Returns:
        Cliente Supabase configurado
    
    Raises:
        EnvironmentError: Si faltan las credenciales
    """
    global _supabase_client
    
    if _supabase_client is None:
        with _lock:
            # Double-check dentro del lock
            if _supabase_client is None:
                # Importar config aqui para evitar circular import
                from infrastructure.config import get_config
                
                config = get_config()
                
                # Crear cliente con credenciales de entorno
                # NUNCA hardcodear las credenciales aqui
                _supabase_client = create_client(
                    config.SUPABASE_URL,
                    config.SUPABASE_KEY
                )
    
    return _supabase_client


def reset_client() -> None:
    """
    Resetea el cliente singleton (solo para testing).
    
    POR QUE RESET:
    - Util en tests para limpiar estado entre pruebas
    - NO usar en produccion
    """
    global _supabase_client
    with _lock:
        _supabase_client = None


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Cliente Supabase ===\n")
    
    try:
        # Intentar obtener el cliente
        client = get_supabase_client()
        print("[OK] Cliente Supabase creado correctamente")
        print(f"     Tipo: {type(client)}")
        
        # Verificar que es singleton
        client2 = get_supabase_client()
        es_mismo = client is client2
        print(f"[OK] Es singleton: {es_mismo}")
        
        # Intentar una operacion simple (health check)
        # Esto verifica que las credenciales son validas
        try:
            # Consulta simple que no requiere datos
            response = client.table('alumnos').select('id').limit(1).execute()
            print("[OK] Conexion a Supabase verificada")
            print(f"     Respuesta: {len(response.data)} registros")
        except Exception as e:
            print(f"[ADVERTENCIA] No se pudo conectar a la tabla alumnos: {e}")
            print("     Esto puede ser normal si la tabla no existe aun")
        
        print("\n=== Prueba pasada ===")
        
    except EnvironmentError as e:
        print(f"[ADVERTENCIA] {e}")
        print("\nEsto es esperado si no tienes un archivo .env configurado.")
        
    except Exception as e:
        print(f"[ERROR] {e}")
