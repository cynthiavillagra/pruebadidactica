/**
 * ===========================================================================
 * APP.JS - App Didactica CRUD de Alumnos
 * ===========================================================================
 * Frontend JavaScript con:
 * - Autenticacion Supabase
 * - Watchdog de sesion (15 minutos de inactividad)
 * - Interceptor de 401 para redirigir a login
 * - CRUD completo de alumnos
 * ===========================================================================
 * 
 * ARQUITECTURA:
 * - Patron Module: Todo encapsulado en objeto App
 * - Event-driven: Listeners para interaccion
 * - Stateless-ready: Token en memoria, no en variables globales persistentes
 * 
 * SEGURIDAD:
 * - Credenciales se cargan de /api/config (NO hardcodeadas)
 * - Token almacenado en memoria (se pierde al cerrar pestana)
 * - Watchdog cierra sesion tras 15 min de inactividad
 * - Interceptor maneja 401 automaticamente
 * 
 * ===========================================================================
 */

// ==========================================================================
// CONFIGURACION - SE CARGA DINAMICAMENTE DESDE /api/config
// ==========================================================================
// POR QUE NO HARDCODEAR:
// - Las credenciales deben venir de variables de entorno
// - El frontend las obtiene del backend via endpoint /api/config
// - SUPABASE_URL y SUPABASE_KEY (anon) son publicas por diseno de Supabase
// - El JWT_SECRET NUNCA se expone al frontend
// ==========================================================================

let SUPABASE_URL = '';
let SUPABASE_ANON_KEY = '';
let SESSION_TIMEOUT_SECONDS = 900;

// ==========================================================================
// INICIALIZACION DE SUPABASE (diferida hasta obtener config)
// ==========================================================================

let supabaseClient = null;

/**
 * Inicializa el cliente Supabase despues de obtener la configuracion.
 */
function initSupabase(url, key) {
    if (typeof supabase !== 'undefined' && url && key) {
        supabaseClient = supabase.createClient(url, key);
        console.log('[Supabase] Cliente inicializado');
        return true;
    }
    console.warn('[Supabase] No se pudo inicializar - config vacia o SDK no disponible');
    return false;
}

// ==========================================================================
// MODULO PRINCIPAL DE LA APLICACION
// ==========================================================================

const App = {
    // Estado de la aplicacion (en memoria, no persistente)
    state: {
        user: null,
        token: null,
        alumnos: [],
        editandoId: null,
        sessionTimer: null,
        sessionSecondsLeft: SESSION_TIMEOUT_SECONDS,
        configLoaded: false
    },

    // ======================================================================
    // INICIALIZACION
    // ======================================================================

    /**
     * Inicializa la aplicacion.
     * Se llama cuando el DOM esta listo.
     */
    async init() {
        console.log('[App] Inicializando...');

        // Cargar configuracion desde el backend
        await this.loadConfig();

        // Configurar event listeners
        this.setupEventListeners();

        // Verificar sesion existente
        this.checkSession();
    },

    /**
     * Carga la configuracion desde /api/config.
     * 
     * POR QUE:
     * - Las credenciales no deben estar en el codigo fuente
     * - Se obtienen dinamicamente del backend
     * - El backend las lee de variables de entorno
     */
    async loadConfig() {
        try {
            const response = await fetch('/api/config');

            if (!response.ok) {
                throw new Error('No se pudo cargar la configuracion');
            }

            const config = await response.json();

            SUPABASE_URL = config.supabase_url;
            SUPABASE_ANON_KEY = config.supabase_key;
            SESSION_TIMEOUT_SECONDS = config.session_timeout || 900;
            this.state.sessionSecondsLeft = SESSION_TIMEOUT_SECONDS;

            // Inicializar Supabase con las credenciales
            initSupabase(SUPABASE_URL, SUPABASE_ANON_KEY);

            this.state.configLoaded = true;
            console.log('[App] Configuracion cargada correctamente');

        } catch (error) {
            console.error('[App] Error cargando configuracion:', error);
            this.toast('Error cargando configuracion del servidor', 'error');
        }
    },

    /**
     * Configura todos los event listeners.
     */
    setupEventListeners() {
        // Login
        document.getElementById('form-login')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Logout
        document.getElementById('btn-logout')?.addEventListener('click', () => {
            this.handleLogout();
        });

        // Navegacion
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.dataset.section;
                this.navigateTo(section);
            });
        });

        // Toggle sidebar (mobile)
        document.getElementById('btn-toggle-sidebar')?.addEventListener('click', () => {
            document.getElementById('sidebar')?.classList.toggle('open');
        });

        // CRUD Alumnos
        document.getElementById('btn-nuevo-alumno')?.addEventListener('click', () => {
            this.mostrarFormulario();
        });

        document.getElementById('btn-refrescar')?.addEventListener('click', () => {
            this.cargarAlumnos();
        });

        document.getElementById('btn-cerrar-form')?.addEventListener('click', () => {
            this.ocultarFormulario();
        });

        document.getElementById('btn-cancelar')?.addEventListener('click', () => {
            this.ocultarFormulario();
        });

        document.getElementById('form-alumno')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.guardarAlumno();
        });

        // Modal de sesion expirada
        document.getElementById('btn-modal-login')?.addEventListener('click', () => {
            this.irALogin();
        });

        // Modal de confirmacion de eliminacion
        document.getElementById('btn-cancelar-eliminar')?.addEventListener('click', () => {
            this.cerrarModalEliminar();
        });

        document.getElementById('btn-confirmar-eliminar')?.addEventListener('click', () => {
            this.confirmarEliminacion();
        });

        // Watchdog: resetear timer en cualquier interaccion
        ['click', 'keypress', 'mousemove', 'scroll'].forEach(event => {
            document.addEventListener(event, () => {
                this.resetSessionTimer();
            });
        });
    },

    // ======================================================================
    // AUTENTICACION
    // ======================================================================

    /**
     * Verifica si hay una sesion activa.
     */
    async checkSession() {
        if (!supabaseClient) {
            console.warn('[App] Supabase no configurado');
            this.mostrarLogin();
            return;
        }

        try {
            const { data: { session } } = await supabaseClient.auth.getSession();

            if (session) {
                this.state.user = session.user;
                this.state.token = session.access_token;
                this.mostrarPrincipal();
            } else {
                this.mostrarLogin();
            }
        } catch (error) {
            console.error('[App] Error verificando sesion:', error);
            this.mostrarLogin();
        }
    },

    /**
     * Maneja el proceso de login.
     */
    async handleLogin() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const errorDiv = document.getElementById('login-error');
        const btn = document.querySelector('#form-login button[type="submit"]');

        // Ocultar error previo
        errorDiv.style.display = 'none';

        // Mostrar loading
        this.setButtonLoading(btn, true);

        try {
            if (!supabaseClient) {
                throw new Error('Supabase no configurado. Verifica SUPABASE_URL y SUPABASE_ANON_KEY en app.js');
            }

            const { data, error } = await supabaseClient.auth.signInWithPassword({
                email,
                password
            });

            if (error) {
                throw error;
            }

            this.state.user = data.user;
            this.state.token = data.session.access_token;

            this.mostrarPrincipal();
            this.toast('Bienvenido/a', 'success');

        } catch (error) {
            console.error('[App] Error en login:', error);
            errorDiv.textContent = error.message || 'Error al iniciar sesion';
            errorDiv.style.display = 'block';
        } finally {
            this.setButtonLoading(btn, false);
        }
    },

    /**
     * Maneja el proceso de logout.
     */
    async handleLogout() {
        try {
            if (supabaseClient) {
                await supabaseClient.auth.signOut();
            }
        } catch (error) {
            console.error('[App] Error en logout:', error);
        }

        this.state.user = null;
        this.state.token = null;
        this.stopSessionTimer();
        this.mostrarLogin();
        this.toast('Sesion cerrada', 'success');
    },

    // ======================================================================
    // WATCHDOG DE SESION (15 minutos de inactividad)
    // ======================================================================

    /**
     * Inicia el timer de sesion.
     */
    startSessionTimer() {
        this.state.sessionSecondsLeft = SESSION_TIMEOUT_SECONDS;
        this.updateSessionDisplay();

        if (this.state.sessionTimer) {
            clearInterval(this.state.sessionTimer);
        }

        this.state.sessionTimer = setInterval(() => {
            this.state.sessionSecondsLeft--;
            this.updateSessionDisplay();

            if (this.state.sessionSecondsLeft <= 0) {
                this.handleSessionExpired();
            }
        }, 1000);
    },

    /**
     * Reinicia el timer de sesion (en cada interaccion).
     */
    resetSessionTimer() {
        if (this.state.user && this.state.sessionSecondsLeft < SESSION_TIMEOUT_SECONDS) {
            this.state.sessionSecondsLeft = SESSION_TIMEOUT_SECONDS;
            this.updateSessionDisplay();
        }
    },

    /**
     * Detiene el timer de sesion.
     */
    stopSessionTimer() {
        if (this.state.sessionTimer) {
            clearInterval(this.state.sessionTimer);
            this.state.sessionTimer = null;
        }
    },

    /**
     * Actualiza el display del timer.
     */
    updateSessionDisplay() {
        const timerElement = document.getElementById('session-timer');
        if (timerElement) {
            const minutes = Math.floor(this.state.sessionSecondsLeft / 60);
            const seconds = this.state.sessionSecondsLeft % 60;
            timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

            // Cambiar color si queda poco tiempo
            const dot = document.querySelector('.session-dot');
            if (this.state.sessionSecondsLeft <= 60) {
                dot?.style.setProperty('background-color', 'var(--danger)');
            } else if (this.state.sessionSecondsLeft <= 180) {
                dot?.style.setProperty('background-color', 'var(--warning)');
            } else {
                dot?.style.setProperty('background-color', 'var(--success)');
            }
        }
    },

    /**
     * Maneja la expiracion de sesion.
     */
    handleSessionExpired() {
        this.stopSessionTimer();
        this.state.user = null;
        this.state.token = null;

        // Mostrar modal de sesion expirada
        document.getElementById('modal-sesion-expirada').style.display = 'flex';
    },

    /**
     * Redirige al login despues del modal.
     */
    irALogin() {
        document.getElementById('modal-sesion-expirada').style.display = 'none';
        this.mostrarLogin();
    },

    // ======================================================================
    // NAVEGACION
    // ======================================================================

    /**
     * Muestra la pantalla de login.
     */
    mostrarLogin() {
        document.getElementById('pantalla-login').style.display = 'flex';
        document.getElementById('pantalla-principal').style.display = 'none';

        // Limpiar formulario
        document.getElementById('form-login')?.reset();
        document.getElementById('login-error').style.display = 'none';
    },

    /**
     * Muestra la pantalla principal.
     */
    mostrarPrincipal() {
        document.getElementById('pantalla-login').style.display = 'none';
        document.getElementById('pantalla-principal').style.display = 'flex';

        // Mostrar email del usuario
        const userEmail = document.getElementById('user-email');
        if (userEmail && this.state.user) {
            userEmail.textContent = this.state.user.email || 'Usuario';
        }

        // Iniciar timer de sesion
        this.startSessionTimer();

        // Cargar alumnos
        this.cargarAlumnos();
    },

    /**
     * Navega a una seccion.
     */
    navigateTo(section) {
        // Actualizar nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.section === section) {
                item.classList.add('active');
            }
        });

        // Mostrar/ocultar secciones
        document.getElementById('seccion-alumnos').style.display =
            section === 'alumnos' ? 'block' : 'none';
        document.getElementById('seccion-docs').style.display =
            section === 'docs' ? 'block' : 'none';

        // Actualizar titulo
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = section === 'alumnos'
                ? 'Gestion de Alumnos'
                : 'Documentacion';
        }

        // Cerrar sidebar en mobile
        document.getElementById('sidebar')?.classList.remove('open');
    },

    // ======================================================================
    // CRUD DE ALUMNOS
    // ======================================================================

    /**
     * Carga la lista de alumnos desde la API.
     */
    async cargarAlumnos() {
        const loading = document.getElementById('tabla-loading');
        const empty = document.getElementById('tabla-vacia');
        const tbody = document.getElementById('tbody-alumnos');

        loading.style.display = 'flex';
        empty.style.display = 'none';
        tbody.innerHTML = '';

        try {
            const response = await this.fetchAPI('/api/alumnos', {
                method: 'GET'
            });

            this.state.alumnos = response;

            if (response.length === 0) {
                empty.style.display = 'flex';
            } else {
                this.renderAlumnos(response);
            }

        } catch (error) {
            console.error('[App] Error cargando alumnos:', error);
            this.toast('Error al cargar alumnos', 'error');
        } finally {
            loading.style.display = 'none';
        }
    },

    /**
     * Renderiza la tabla de alumnos.
     */
    renderAlumnos(alumnos) {
        const tbody = document.getElementById('tbody-alumnos');
        tbody.innerHTML = '';

        alumnos.forEach(alumno => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${this.escapeHtml(alumno.apellido)}</td>
                <td>${this.escapeHtml(alumno.nombre)}</td>
                <td>${this.escapeHtml(alumno.dni)}</td>
                <td class="table-actions">
                    <button class="btn btn-secondary" onclick="App.editarAlumno('${alumno.id}')">
                        ✏️ Editar
                    </button>
                    <button class="btn btn-danger" onclick="App.eliminarAlumno('${alumno.id}')">
                        🗑️ Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    },

    /**
     * Muestra el formulario para nuevo/editar alumno.
     */
    mostrarFormulario(alumno = null) {
        const container = document.getElementById('form-container');
        const titulo = document.getElementById('form-titulo');
        const form = document.getElementById('form-alumno');

        form.reset();
        document.getElementById('form-error').style.display = 'none';

        if (alumno) {
            titulo.textContent = 'Editar Alumno';
            document.getElementById('alumno-id').value = alumno.id;
            document.getElementById('alumno-nombre').value = alumno.nombre;
            document.getElementById('alumno-apellido').value = alumno.apellido;
            document.getElementById('alumno-dni').value = alumno.dni;
            this.state.editandoId = alumno.id;
        } else {
            titulo.textContent = 'Nuevo Alumno';
            this.state.editandoId = null;
        }

        container.style.display = 'block';
        document.getElementById('alumno-nombre').focus();
    },

    /**
     * Oculta el formulario.
     */
    ocultarFormulario() {
        document.getElementById('form-container').style.display = 'none';
        this.state.editandoId = null;
    },

    /**
     * Guarda un alumno (crear o actualizar).
     */
    async guardarAlumno() {
        const nombre = document.getElementById('alumno-nombre').value.trim();
        const apellido = document.getElementById('alumno-apellido').value.trim();
        const dni = document.getElementById('alumno-dni').value.trim();
        const errorDiv = document.getElementById('form-error');
        const btn = document.querySelector('#form-alumno button[type="submit"]');

        errorDiv.style.display = 'none';
        this.setButtonLoading(btn, true);

        try {
            const data = { nombre, apellido, dni };
            let response;

            if (this.state.editandoId) {
                // Actualizar
                response = await this.fetchAPI(`/api/alumnos/${this.state.editandoId}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                this.toast('Alumno actualizado correctamente', 'success');
            } else {
                // Crear
                response = await this.fetchAPI('/api/alumnos', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                this.toast('Alumno creado correctamente', 'success');
            }

            this.ocultarFormulario();
            this.cargarAlumnos();

        } catch (error) {
            console.error('[App] Error guardando alumno:', error);
            errorDiv.textContent = error.message || 'Error al guardar';
            errorDiv.style.display = 'block';
        } finally {
            this.setButtonLoading(btn, false);
        }
    },

    /**
     * Prepara la edicion de un alumno.
     */
    editarAlumno(id) {
        const alumno = this.state.alumnos.find(a => a.id === id);
        if (alumno) {
            this.mostrarFormulario(alumno);
        }
    },

    /**
     * Abre el modal de confirmacion de eliminacion.
     */
    eliminarAlumno(id) {
        const alumno = this.state.alumnos.find(a => a.id === id);
        if (alumno) {
            this.state.editandoId = id;
            document.getElementById('mensaje-eliminar').textContent =
                `¿Seguro que desea eliminar a ${alumno.nombre} ${alumno.apellido}?`;
            document.getElementById('modal-confirmar-eliminar').style.display = 'flex';
        }
    },

    /**
     * Cierra el modal de confirmacion.
     */
    cerrarModalEliminar() {
        document.getElementById('modal-confirmar-eliminar').style.display = 'none';
        this.state.editandoId = null;
    },

    /**
     * Confirma y ejecuta la eliminacion.
     */
    async confirmarEliminacion() {
        const id = this.state.editandoId;
        this.cerrarModalEliminar();

        try {
            await this.fetchAPI(`/api/alumnos/${id}`, {
                method: 'DELETE'
            });

            this.toast('Alumno eliminado correctamente', 'success');
            this.cargarAlumnos();

        } catch (error) {
            console.error('[App] Error eliminando alumno:', error);
            this.toast('Error al eliminar alumno', 'error');
        }
    },

    // ======================================================================
    // HTTP CLIENT CON INTERCEPTOR DE 401
    // ======================================================================

    /**
     * Realiza una peticion a la API con autenticacion.
     * Incluye interceptor de 401 para manejar sesiones expiradas.
     */
    async fetchAPI(url, options = {}) {
        // Agregar headers por defecto
        options.headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Agregar token de autenticacion si existe
        if (this.state.token) {
            options.headers['Authorization'] = `Bearer ${this.state.token}`;
        }

        try {
            const response = await fetch(url, options);

            // Interceptor de 401: sesion expirada
            if (response.status === 401) {
                const data = await response.json();

                // Si es SESSION_EXPIRED, mostrar modal
                if (data.codigo === 'SESSION_EXPIRED') {
                    this.handleSessionExpired();
                    throw new Error('Sesion expirada');
                }

                throw new Error(data.error || 'No autorizado');
            }

            // Manejar otros errores
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || `Error ${response.status}`);
            }

            // Respuesta exitosa
            // DELETE retorna 204 sin contenido
            if (response.status === 204) {
                return null;
            }

            return await response.json();

        } catch (error) {
            // Re-throw para que el llamador maneje el error
            throw error;
        }
    },

    // ======================================================================
    // UTILIDADES
    // ======================================================================

    /**
     * Muestra/oculta estado de loading en un boton.
     */
    setButtonLoading(btn, loading) {
        if (!btn) return;

        const text = btn.querySelector('.btn-text');
        const spinner = btn.querySelector('.btn-loading');

        if (loading) {
            btn.disabled = true;
            if (text) text.style.display = 'none';
            if (spinner) spinner.style.display = 'inline';
        } else {
            btn.disabled = false;
            if (text) text.style.display = 'inline';
            if (spinner) spinner.style.display = 'none';
        }
    },

    /**
     * Escapa HTML para prevenir XSS.
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Muestra un toast/notificacion.
     */
    toast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        container.appendChild(toast);

        // Auto-remover despues de 3 segundos
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
};

// ==========================================================================
// INICIAR CUANDO EL DOM ESTE LISTO
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
