# Manual Tecnico: api/index.py

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: API (Capa de Presentacion - Entry Point)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este archivo es el **punto de entrada de la aplicacion**. Configura Flask, registra blueprints, y expone la variable `app` que Vercel y otros servidores WSGI necesitan.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | API Layer - Entry Point |
| **Requisitos No Funcionales** | RNF (Compatibilidad multiplataforma) |
| **Patron** | Factory Pattern, WSGI |

### 1.3 Compatibilidad

| Plataforma | Como Usa Este Archivo |
|------------|----------------------|
| **Local** | `python api/index.py` |
| **Vercel** | Detecta variable `app` |
| **Docker/Gunicorn** | `gunicorn api.index:app` |

---

## 2. Estrategia de Construccion

### 2.1 Orden de Ejecucion

```
1. Cargar dotenv (ANTES de imports)
2. Imports de Flask y rutas
3. create_app() crea y configura Flask
4. Variable global 'app' creada
5. if __main__: ejecuta servidor dev
```

### 2.2 Por Que dotenv AL PRINCIPIO

```python
# PASO 1: CARGAR VARIABLES DE ENTORNO (ANTES DE TODO)
from dotenv import load_dotenv
load_dotenv()

# PASO 2: AHORA SI LOS IMPORTS
from api.routes import api_bp
```

**Razon**: Los modulos de infraestructura (config.py) necesitan las variables disponibles al importarse.

---

## 3. Aclaracion Metodologica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` ejecuta el **servidor de desarrollo** de Flask:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
```

**SOLO para desarrollo local**:
- Hot reload al modificar archivos
- Mensajes de error detallados
- NUNCA usar en produccion

### 3.2 Variable app (WSGI)

```python
app = create_app()
```

**Por que variable global**:
- Vercel busca `app` en `api/index.py`
- Gunicorn necesita `api.index:app`
- Es la CONFIGURACION, no el ESTADO (no viola stateless)

---

## 4. Codigo Fuente

### 4.1 Factory Function

```python
def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder=str(ROOT_DIR / 'static'),
        static_url_path='/static'
    )
    
    # Configuracion
    app.config['JSON_SORT_KEYS'] = False
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Ruta para servir el frontend
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    return app
```

### 4.2 Servir Estaticos

```python
@app.route('/<path:path>')
def serve_static(path):
    static_file = ROOT_DIR / 'static' / path
    if static_file.exists():
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')
```

**Por que catch-all**:
- Sirve archivos CSS, JS, imagenes
- Fallback a index.html (para SPA)

---

## 5. Prueba de Fuego

### 5.1 Comando de Ejecucion

```powershell
python api/index.py
```

### 5.2 Salida Esperada

```
============================================================
  APP DIDACTICA CRUD - Servidor Local
============================================================
  URL: http://localhost:5000
  API: http://localhost:5000/api/health
============================================================
  Presiona Ctrl+C para detener
============================================================
 * Running on http://0.0.0.0:5000
 * Restarting with stat
 * Debugger is active!
```

### 5.3 Verificacion

```powershell
# En otra terminal
curl http://localhost:5000/api/health
# Debe retornar: {"status": "healthy", ...}

start http://localhost:5000
# Debe abrir el frontend
```

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Factory function | Permite crear multiples apps (testing) |
| dotenv al inicio | Variables disponibles para todos |
| Variable app global | Compatibilidad WSGI |
| Servir estaticos | Todo en un servidor |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| Crear app en import | Dificil de testear |
| Servidor separado para estaticos | Complejidad |
| Variables en create_app() | Carga tardia |
| Configuracion en diccionario | Menos tipado |

---

## 7. Guia de Resolucion de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `Address already in use` | Puerto ocupado | Cambiar PORT en .env |
| `ModuleNotFoundError` | Import incorrecto | Ejecutar desde raiz |
| `SUPABASE_URL required` | .env no existe | Crear .env |
| Estaticos no cargan | Path incorrecto | Verificar static_folder |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel | Docker |
|---------|-------|--------|--------|
| Entry point | `python api/index.py` | Variable `app` | `gunicorn api.index:app` |
| Debug | Activado | Desactivado | Desactivado |
| Hot reload | Si | No | No |
| Puerto | 5000 | Dinamico | 8000 |
| Servidor | Flask dev | Vercel runtime | Gunicorn |

### 7.3 Configuracion vercel.json

```json
{
  "builds": [
    {"src": "api/index.py", "use": "@vercel/python"}
  ],
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"src": "/(.*)", "dest": "api/index.py"}
  ]
}
```

---

> **Manual Tecnico**: api/index.py  
> **Version**: 1.0.0
