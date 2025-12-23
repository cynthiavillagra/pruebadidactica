# 📦 Manual Técnico: requirements.txt

> **Archivo**: `requirements.txt`  
> **Tipo**: Configuración de Dependencias  
> **Fase**: 4-A (Setup Local)  
> **Fecha**: 2025-12-22

---

## 1. Propósito

### 1.1 Descripción

El archivo `requirements.txt` define todas las dependencias Python necesarias para ejecutar la aplicación. Es el estándar de la industria para proyectos Python.

### 1.2 Trazabilidad Completa

| Aspecto | Valor |
|---------|-------|
| **Módulo** | SISTEMA (Configuración) |
| **Historia de Usuario** | N/A (Infraestructura) |
| **Requisito No Funcional** | RNF-004 (Portabilidad) |
| **Criterio de Aceptación** | La aplicación debe funcionar en local, Vercel y Docker |

---

## 2. Estrategia de Construcción

### 2.1 Principios Aplicados

| Principio | Aplicación |
|-----------|------------|
| **Mínimas dependencias** | Solo lo necesario, nada superfluo |
| **Versiones mínimas** | Usar `>=` para permitir actualizaciones de seguridad |
| **Documentación inline** | Cada dependencia explica POR QUÉ se eligió |
| **Compatibilidad** | Verificado para local, Vercel y Docker |

### 2.2 Dependencias Incluidas

| Categoría | Paquete | Versión | Propósito |
|-----------|---------|---------|-----------|
| **Web** | Flask | >=3.0.0 | Framework web |
| **Web** | Werkzeug | >=3.0.0 | Toolkit WSGI |
| **Config** | python-dotenv | >=1.0.0 | Variables de entorno |
| **BD** | supabase | >=2.0.0 | Cliente Supabase |
| **Auth** | PyJWT | >=2.8.0 | Validación JWT |
| **Utils** | python-dateutil | >=2.8.0 | Manejo de fechas |
| **Test** | pytest | >=8.0.0 | Testing |
| **Test** | pytest-cov | >=4.0.0 | Cobertura |
| **Dev** | httpx | >=0.25.0 | Cliente HTTP |

---

## 3. Aclaración Metodológica

### 3.1 ¿Por qué `>=` y no `==`?

```txt
# ❌ EVITAR: Versiones exactas (excepto casos especiales)
Flask==3.0.0

# ✅ PREFERIR: Versiones mínimas
Flask>=3.0.0
```

**Razón**: Las versiones mínimas permiten recibir actualizaciones de seguridad automáticamente al hacer `pip install --upgrade`.

### 3.2 ¿Por qué comentarios en requirements.txt?

Los comentarios `# POR QUÉ` sirven para:
1. **Documentar decisiones** sin necesidad de archivo separado
2. **Facilitar onboarding** de nuevos desarrolladores
3. **Justificar elecciones** cuando hay alternativas

---

## 4. Código Fuente

```txt
# ═══════════════════════════════════════════════════════════════════════════
# REQUIREMENTS.TXT - Dependencias del Proyecto
# ═══════════════════════════════════════════════════════════════════════════

# CORE: Framework Web
Flask>=3.0.0
Werkzeug>=3.0.0

# CONFIGURACIÓN: Variables de Entorno
python-dotenv>=1.0.0

# BASE DE DATOS: Cliente Supabase
supabase>=2.0.0

# SEGURIDAD: JWT
PyJWT>=2.8.0

# UTILIDADES
python-dateutil>=2.8.0

# TESTING
pytest>=8.0.0
pytest-cov>=4.0.0
httpx>=0.25.0
```

---

## 5. Prueba de Fuego

### 5.1 Verificación de Instalación

```powershell
# 1. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar instalación
pip list

# 4. Verificar imports críticos
python -c "import flask; print(f'Flask {flask.__version__}')"
python -c "import dotenv; print('python-dotenv OK')"
python -c "import supabase; print('supabase OK')"
python -c "import jwt; print(f'PyJWT {jwt.__version__}')"
python -c "import pytest; print(f'pytest {pytest.__version__}')"
```

### 5.2 Salida Esperada

```
Flask 3.x.x
python-dotenv OK
supabase OK
PyJWT 2.x.x
pytest 8.x.x
```

### 5.3 Criterios de Éxito

| Criterio | Verificación |
|----------|--------------|
| ✅ Sin errores de instalación | `pip install` termina sin errores |
| ✅ Todos los imports funcionan | Los comandos `python -c` no dan error |
| ✅ Versiones correctas | Las versiones son >= a las especificadas |

---

## 6. Análisis Dual

### 6.1 ¿Por qué SÍ estas dependencias?

| Dependencia | Por qué SÍ |
|-------------|------------|
| **Flask** | Micro-framework, mínima magia, ideal para didáctica |
| **python-dotenv** | Estándar para 12-factor apps, separa config de código |
| **supabase** | Cliente oficial, integración nativa con Auth y RLS |
| **PyJWT** | Simple, ligero, solo para validar tokens |
| **pytest** | Estándar de la industria, sintaxis limpia |

### 6.2 ¿Por qué NO alternativas?

| Alternativa | Por qué NO |
|-------------|------------|
| **Django** | Demasiado pesado para CRUD simple, oculta HTTP |
| **FastAPI** | Requiere async, añade complejidad innecesaria |
| **SQLAlchemy** | No necesario, Supabase maneja la BD |
| **requests** | httpx es más moderno y mejor para testing |
| **unittest** | pytest tiene sintaxis más limpia |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `pip: command not found` | Python no en PATH | Reinstalar Python marcando "Add to PATH" |
| `No module named flask` | Entorno no activado | Activar venv: `.\venv\Scripts\Activate` |
| `ImportError: supabase` | Falta instalar | `pip install -r requirements.txt` |
| `Version conflict` | Dependencias incompatibles | `pip install --upgrade pip` y reinstalar |
| `Permission denied` (Linux) | Sin permisos | Usar `pip install --user` |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel | Docker |
|---------|-------|--------|--------|
| **Instalación** | `pip install -r` | Automático | `RUN pip install -r` |
| **Entorno virtual** | Requerido | No aplica | No aplica |
| **Versión Python** | 3.10+ local | runtime en vercel.json | FROM python:3.11 |

---

## 8. Checklist de Calidad

| Check | Estado |
|-------|--------|
| 🔒 **Auditoría de Secretos** | ✅ No hay secretos en este archivo |
| ☁️ **Compatibilidad Serverless** | ✅ Todas las dependencias son compatibles con Vercel |
| 🧪 **Prueba atómica presente** | ✅ Comandos de verificación documentados |
| 📝 **Comentarios justificativos** | ✅ Cada dependencia tiene "POR QUÉ" |

---

> **Manual generado**: 2025-12-22  
> **Siguiente archivo**: `.gitignore`
