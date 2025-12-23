# Manual Tecnico: Frontend (static/index.html, css/styles.css, js/app.js)

> **Proyecto**: App Didactica CRUD de Alumnos  
> **Modulo**: Presentation (Frontend)  
> **Fecha**: 2025-12-22

---

## 1. Proposito

### 1.1 Descripcion

Este manual cubre los tres archivos del **frontend**: HTML, CSS y JavaScript. Implementan la interfaz de usuario con login, CRUD de alumnos, watchdog de sesion y visor de documentacion.

### 1.2 Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Modulo** | Presentation Layer - Frontend |
| **Historias de Usuario** | HU-001, HU-002, HU-003, HU-004, HU-005 |
| **Requisitos Funcionales** | RF-001 a RF-010 |
| **Requisitos No Funcionales** | RNF-002 (Intuitivo), RNF-004 (Responsive), RNF-008 (Sesion) |

---

## 2. static/index.html

### 2.1 Proposito

Estructura HTML de la aplicacion: login, CRUD, modales y navegacion.

### 2.2 Secciones Principales

| Seccion | ID | Proposito |
|---------|-----|-----------|
| Modal sesion expirada | `modal-sesion-expirada` | Aviso de timeout |
| Modal eliminar | `modal-confirmar-eliminar` | Confirmacion RF-009 |
| Pantalla login | `pantalla-login` | Autenticacion |
| Pantalla principal | `pantalla-principal` | CRUD alumnos |
| Sidebar | `sidebar` | Navegacion |
| Seccion alumnos | `seccion-alumnos` | Lista y formulario |
| Seccion docs | `seccion-docs` | Visor documentacion |

### 2.3 Por Que HTML Semantico

- `<header>`, `<main>`, `<aside>`, `<section>` para accesibilidad
- IDs unicos para cada elemento interactivo
- Formularios con `required` para validacion nativa

---

## 3. static/css/styles.css

### 3.1 Proposito

Estilos CSS con modo oscuro, variables CSS, diseño responsive.

### 3.2 Variables CSS

```css
:root {
    --primary: #6366f1;
    --bg-primary: #0f172a;
    --text-primary: #f8fafc;
    --sidebar-width: 260px;
    --transition-fast: 0.15s ease;
}
```

### 3.3 Componentes

| Componente | Clase | Uso |
|------------|-------|-----|
| Botones | `.btn`, `.btn-primary` | Acciones |
| Cards | `.card` | Contenedores |
| Formularios | `.form-group` | Inputs |
| Tabla | `.table` | Lista alumnos |
| Modal | `.modal` | Dialogos |
| Toast | `.toast` | Notificaciones |

### 3.4 Responsive

```css
@media (max-width: 768px) {
    .sidebar { transform: translateX(-100%); }
    .main-content { margin-left: 0; }
}
```

---

## 4. static/js/app.js

### 4.1 Proposito

Logica JavaScript: autenticacion, CRUD, watchdog e interceptor 401.

### 4.2 Arquitectura

```
App (objeto principal)
|-- state: { user, token, alumnos, ... }
|-- init(): Inicializacion
|-- loadConfig(): Carga credenciales de /api/config
|-- setupEventListeners(): Configura eventos
|-- checkSession(): Verifica sesion Supabase
|-- handleLogin(): Login
|-- handleLogout(): Logout
|-- startSessionTimer(): Watchdog
|-- cargarAlumnos(): GET /api/alumnos
|-- guardarAlumno(): POST/PUT
|-- eliminarAlumno(): DELETE
|-- fetchAPI(): HTTP client con interceptor
```

### 4.3 Carga Dinamica de Config

```javascript
async loadConfig() {
    const response = await fetch('/api/config');
    const config = await response.json();
    
    SUPABASE_URL = config.supabase_url;
    SUPABASE_ANON_KEY = config.supabase_key;
    
    initSupabase(SUPABASE_URL, SUPABASE_ANON_KEY);
}
```

**Por que dinamico**:
- Credenciales NO hardcodeadas en el codigo
- Se obtienen del backend (variables de entorno)
- SUPABASE_KEY es publica por diseno de Supabase

### 4.4 Watchdog de Sesion

```javascript
startSessionTimer() {
    this.state.sessionSecondsLeft = SESSION_TIMEOUT_SECONDS;
    
    this.state.sessionTimer = setInterval(() => {
        this.state.sessionSecondsLeft--;
        this.updateSessionDisplay();
        
        if (this.state.sessionSecondsLeft <= 0) {
            this.handleSessionExpired();
        }
    }, 1000);
}

resetSessionTimer() {
    if (this.state.user) {
        this.state.sessionSecondsLeft = SESSION_TIMEOUT_SECONDS;
    }
}
```

**Eventos que resetean**:
- `click`, `keypress`, `mousemove`, `scroll`

### 4.5 Interceptor 401

```javascript
async fetchAPI(url, options = {}) {
    const response = await fetch(url, options);
    
    if (response.status === 401) {
        const data = await response.json();
        
        if (data.codigo === 'SESSION_EXPIRED') {
            this.handleSessionExpired();
            throw new Error('Sesion expirada');
        }
        
        throw new Error('No autorizado');
    }
    
    return await response.json();
}
```

---

## 5. Prueba de Fuego

### 5.1 Verificar Frontend

```powershell
python api/index.py
start http://localhost:5000
```

### 5.2 Checklist Visual

| Verificacion | Esperado |
|--------------|----------|
| Pantalla de login | Visible con fondo oscuro |
| CSS cargado | Estilos aplicados |
| Logo visible | Emoji 📚 |
| Formulario funcional | Campos nombre, email, password |
| Consola sin errores | [App] Inicializando... |

### 5.3 Checklist Funcional (con Supabase)

| Verificacion | Esperado |
|--------------|----------|
| Login | Redirige a pantalla principal |
| Timer visible | 15:00 en header |
| Listar alumnos | Tabla con datos |
| Crear alumno | Toast "creado" |
| Editar alumno | Formulario pre-cargado |
| Eliminar | Modal de confirmacion |
| Timeout | Modal "Sesion Expirada" despues de 15 min |

---

## 6. Analisis Dual

### 6.1 Por Que SI Esta Implementacion

| Decision | Justificacion |
|----------|---------------|
| Un solo archivo JS | Simplicidad para proyecto educativo |
| Vanilla JS | Sin dependencias, mas didactico |
| Patron Module (App) | Encapsula estado y metodos |
| CSS variables | Facil personalizacion |
| Modo oscuro | Tendencia moderna, menos fatiga visual |

### 6.2 Por Que NO Alternativas

| Alternativa Rechazada | Razon |
|----------------------|-------|
| React/Vue | Overkill para CRUD simple |
| jQuery | Obsoleto, mas pesado |
| SASS/LESS | Complejidad innecesaria |
| TailwindCSS | Requiere build paso |
| Token en localStorage | Menos seguro que memoria |

---

## 7. Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| CSS no carga | Path incorrecto | Verificar /static/ |
| JS error "supabase undefined" | SDK no cargo | Verificar CDN |
| Login falla | Credenciales incorrectas | Verificar .env |
| Timer no aparece | Usuario no logueado | Verificar login |
| 401 en todas las peticiones | Token expirado | Re-login |

---

> **Manual Tecnico**: Frontend  
> **Version**: 1.0.0
