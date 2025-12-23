# ===========================================================================
# Entry Point de la Aplicacion
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: API (Presentacion)
# Compatible: Local, Vercel, Docker
# ===========================================================================
#
# ARQUITECTURA MULTIPLATAFORMA:
# - Local: Ejecutar con python api/index.py
# - Vercel: Expone variable 'app' que Vercel detecta automaticamente
# - Docker: Ejecutar con gunicorn api.index:app
#
# REGLA CRITICA:
# - load_dotenv() DEBE ejecutarse ANTES de cualquier import que use config
# - NUNCA hardcodear credenciales
#
# STATELESS:
# - Esta app es 100% stateless
# - No guarda sesiones en variables globales
# - Compatible con serverless (cada request es independiente)
#
# ===========================================================================

"""
Entry point de la aplicacion Flask.

Configura la app y expone los endpoints.
Compatible con Local, Vercel y Docker.
"""

# ===========================================================================
# PASO 1: CARGAR VARIABLES DE ENTORNO (ANTES DE TODO)
# ===========================================================================
# POR QUE AL INICIO:
# - Las variables deben estar disponibles antes de importar otros modulos
# - infrastructure/config.py las necesita inmediatamente
# ===========================================================================

import os
import sys
from pathlib import Path

# Agregar directorio raiz al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()


# ===========================================================================
# PASO 2: IMPORTS (DESPUES DE load_dotenv)
# ===========================================================================

from flask import Flask, send_from_directory

from api.routes import api_bp


# ===========================================================================
# PASO 3: CREAR Y CONFIGURAR LA APP
# ===========================================================================

def create_app() -> Flask:
    """
    Factory function para crear la aplicacion Flask.
    
    POR QUE FACTORY:
    - Permite crear multiples instancias (testing)
    - Configuracion centralizada
    - Patron recomendado por Flask
    
    Returns:
        Aplicacion Flask configurada
    """
    app = Flask(
        __name__,
        static_folder=str(ROOT_DIR / 'static'),
        static_url_path='/static'
    )
    
    # Configuracion
    app.config['JSON_SORT_KEYS'] = False  # Mantener orden de keys
    
    # Importar config solo si esta disponible
    try:
        from infrastructure.config import get_config
        config = get_config()
        app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY
        app.config['DEBUG'] = config.FLASK_DEBUG
    except Exception:
        # En caso de que no haya .env (ej: solo ejecutando tests)
        app.config['SECRET_KEY'] = 'dev-secret-key'
        app.config['DEBUG'] = True
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Ruta para servir el frontend
    @app.route('/')
    def index():
        """Sirve la pagina principal del frontend."""
        return send_from_directory(app.static_folder, 'index.html')
    
    # Ruta catch-all para SPA (si se necesita en el futuro)
    @app.route('/<path:path>')
    def serve_static(path):
        """Sirve archivos estaticos o retorna index.html."""
        static_file = ROOT_DIR / 'static' / path
        if static_file.exists():
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app


# ===========================================================================
# PASO 4: CREAR INSTANCIA DE LA APP
# ===========================================================================
# POR QUE VARIABLE GLOBAL 'app':
# - Vercel busca una variable llamada 'app' en api/index.py
# - Gunicorn tambien la necesita: gunicorn api.index:app
# - Es el patron estandar para WSGI
#
# NOTA STATELESS:
# - La variable 'app' es la CONFIGURACION, no el ESTADO
# - Cada request crea su propio contexto
# - No viola la regla stateless
# ===========================================================================

app = create_app()


# ===========================================================================
# PASO 5: ENTRY POINT PARA EJECUCION LOCAL
# ===========================================================================

if __name__ == '__main__':
    # Obtener puerto de entorno o usar default
    port = int(os.getenv('PORT', 5000))
    
    print("=" * 60)
    print("  APP DIDACTICA CRUD - Servidor Local")
    print("=" * 60)
    print(f"  URL: http://localhost:{port}")
    print(f"  API: http://localhost:{port}/api/health")
    print("=" * 60)
    print("  Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # Ejecutar servidor de desarrollo
    # POR QUE DEBUG=True EN LOCAL:
    # - Hot reload al modificar archivos
    # - Mensajes de error detallados
    # - NUNCA usar en produccion
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
