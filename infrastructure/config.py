# ===========================================================================
# Configuracion de la Aplicacion
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Infrastructure
# ===========================================================================
#
# POR QUE UN MODULO DE CONFIGURACION:
# - Centraliza toda la configuracion en un solo lugar
# - Valida que las variables de entorno esten presentes
# - Falla rapido si falta configuracion (mejor al iniciar que en runtime)
#
# REGLA DE SEGURIDAD:
# - NUNCA hardcodear credenciales
# - Siempre usar os.getenv()
#
# ===========================================================================

"""
Modulo de configuracion centralizada.

Carga y valida todas las variables de entorno necesarias.
"""

# Configuracion de path para pruebas atomicas
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
# POR QUE AL INICIO: Garantiza que las variables esten disponibles
# antes de que cualquier otro modulo las necesite
load_dotenv()


class Config:
    """
    Clase de configuracion con validacion.
    
    POR QUE CLASE Y NO DICCIONARIO:
    - Autocompletado en IDEs
    - Validacion en tiempo de carga
    - Tipado estatico para errores tempranos
    
    Atributos:
        SUPABASE_URL: URL del proyecto Supabase
        SUPABASE_KEY: API Key publica (anon)
        SUPABASE_JWT_SECRET: Secreto para validar JWT
        FLASK_ENV: Entorno (development/production)
        FLASK_DEBUG: Modo debug activo
        FLASK_SECRET_KEY: Clave secreta de Flask
        PORT: Puerto del servidor
        SESSION_TIMEOUT_SECONDS: Timeout de inactividad
    """
    
    def __init__(self):
        """
        Inicializa la configuracion cargando variables de entorno.
        
        Raises:
            EnvironmentError: Si falta alguna variable requerida
        """
        # Supabase (requeridas)
        self.SUPABASE_URL = self._get_required('SUPABASE_URL')
        self.SUPABASE_KEY = self._get_required('SUPABASE_KEY')
        self.SUPABASE_JWT_SECRET = self._get_required('SUPABASE_JWT_SECRET')
        
        # Flask (con defaults)
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'development')
        self.FLASK_DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
        self.FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
        self.PORT = int(os.getenv('PORT', '5000'))
        
        # Seguridad
        self.SESSION_TIMEOUT_SECONDS = int(os.getenv('SESSION_TIMEOUT_SECONDS', '900'))
    
    def _get_required(self, key: str) -> str:
        """
        Obtiene una variable de entorno requerida.
        
        Args:
            key: Nombre de la variable
        
        Returns:
            Valor de la variable
        
        Raises:
            EnvironmentError: Si la variable no existe o esta vacia
        """
        value = os.getenv(key)
        
        if not value:
            raise EnvironmentError(
                f"Variable de entorno '{key}' no configurada.\n"
                f"Por favor, crea un archivo .env basandote en .env.example"
            )
        
        return value
    
    @property
    def is_development(self) -> bool:
        """Indica si estamos en entorno de desarrollo."""
        return self.FLASK_ENV == 'development'
    
    @property
    def is_production(self) -> bool:
        """Indica si estamos en entorno de produccion."""
        return self.FLASK_ENV == 'production'
    
    def to_safe_dict(self) -> dict:
        """
        Retorna la configuracion sin secretos (para logging).
        
        POR QUE SAFE_DICT:
        - Para poder loggear la configuracion sin exponer secretos
        """
        return {
            'SUPABASE_URL': self.SUPABASE_URL,
            'SUPABASE_KEY': f"{self.SUPABASE_KEY[:20]}...(oculto)",
            'FLASK_ENV': self.FLASK_ENV,
            'FLASK_DEBUG': self.FLASK_DEBUG,
            'PORT': self.PORT,
            'SESSION_TIMEOUT_SECONDS': self.SESSION_TIMEOUT_SECONDS
        }


# Instancia global de configuracion
# POR QUE GLOBAL:
# - Se valida una sola vez al importar
# - Si falta config, falla inmediatamente
# - Evita cargar .env multiples veces
#
# NOTA: Esto es seguro en serverless porque es inmutable
try:
    config = Config()
except EnvironmentError as e:
    # En desarrollo, mostrar error amigable
    print(f"\n[ERROR DE CONFIGURACION]\n{e}\n")
    # Crear config dummy para que no falle el import
    # (util para generar documentacion, tests sin .env, etc.)
    config = None


def get_config() -> Config:
    """
    Obtiene la configuracion validada.
    
    Returns:
        Instancia de Config
    
    Raises:
        EnvironmentError: Si la configuracion no fue inicializada
    """
    if config is None:
        raise EnvironmentError(
            "Configuracion no inicializada. "
            "Verifica que el archivo .env exista y tenga las variables requeridas."
        )
    return config


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Configuracion ===\n")
    
    try:
        cfg = get_config()
        print("[OK] Configuracion cargada correctamente")
        print(f"\nConfiguracion (sin secretos):")
        for key, value in cfg.to_safe_dict().items():
            print(f"  {key}: {value}")
        
        print(f"\n  is_development: {cfg.is_development}")
        print(f"  is_production: {cfg.is_production}")
        
        print("\n=== Prueba pasada ===")
        
    except EnvironmentError as e:
        print(f"[ADVERTENCIA] {e}")
        print("\nEsto es esperado si no tienes un archivo .env configurado.")
        print("Crea uno basandote en .env.example")
