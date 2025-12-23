# ===========================================================================
# Excepciones de Dominio
# ===========================================================================
# Proyecto: App Didactica CRUD de Alumnos
# Capa: Domain (Nucleo)
# ===========================================================================
#
# POR QUE EXCEPCIONES PERSONALIZADAS:
# - Permiten manejar errores de negocio de forma especifica
# - El servicio puede lanzar errores semanticos (DNIDuplicado vs Exception)
# - Facilitan el mapeo a codigos HTTP en la capa de presentacion
#
# ===========================================================================

"""
Excepciones personalizadas del dominio.

Este modulo define excepciones especificas para errores de negocio,
permitiendo un manejo de errores semantico y tipado.
"""


class DomainException(Exception):
    """
    Clase base para todas las excepciones de dominio.
    
    POR QUE CLASE BASE:
    - Permite capturar todas las excepciones de dominio con un solo except
    - Facilita agregar comportamiento comun (logging, etc.)
    """
    
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convierte la excepcion a diccionario para respuestas JSON."""
        return {
            "error": self.message,
            "codigo": self.code
        }


class ValidacionError(DomainException):
    """
    Error de validacion de datos de entrada.
    
    Uso: Cuando los datos no cumplen las reglas de negocio.
    HTTP: 400 Bad Request
    """
    
    def __init__(self, message: str, campo: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.campo = campo
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.campo:
            result["campo"] = self.campo
        return result


class AlumnoNoEncontrado(DomainException):
    """
    Error cuando no se encuentra un alumno.
    
    Uso: Cuando se busca por ID y no existe.
    HTTP: 404 Not Found
    """
    
    def __init__(self, identificador: str = None):
        message = "Alumno no encontrado"
        if identificador:
            message = f"Alumno con ID '{identificador}' no encontrado"
        super().__init__(message, "ALUMNO_NOT_FOUND")
        self.identificador = identificador


class DNIDuplicado(DomainException):
    """
    Error cuando el DNI ya existe en el sistema.
    
    Uso: Al crear o actualizar con DNI que ya pertenece a otro alumno.
    HTTP: 409 Conflict
    """
    
    def __init__(self, dni: str = None):
        message = "El DNI ya esta registrado"
        if dni:
            message = f"El DNI '{dni}' ya esta registrado"
        super().__init__(message, "DNI_DUPLICADO")
        self.dni = dni


class RepositoryError(DomainException):
    """
    Error de acceso a datos/repositorio.
    
    Uso: Cuando falla la comunicacion con la base de datos.
    HTTP: 500 Internal Server Error
    """
    
    def __init__(self, message: str = "Error al acceder a los datos"):
        super().__init__(message, "REPOSITORY_ERROR")


class AuthenticationError(DomainException):
    """
    Error de autenticacion.
    
    Uso: Token invalido, expirado o ausente.
    HTTP: 401 Unauthorized
    """
    
    def __init__(self, message: str = "No autenticado"):
        super().__init__(message, "AUTH_ERROR")


class SessionExpiredError(AuthenticationError):
    """
    Error especifico de sesion expirada por inactividad.
    
    Uso: Cuando el watchdog detecta inactividad de 15 minutos.
    HTTP: 401 Unauthorized
    """
    
    def __init__(self):
        super().__init__("Sesion expirada por inactividad")
        self.code = "SESSION_EXPIRED"


# ===========================================================================
# PRUEBA ATOMICA
# ===========================================================================
if __name__ == "__main__":
    print("=== Prueba de Excepciones de Dominio ===\n")
    
    # Test 1: ValidacionError
    try:
        raise ValidacionError("El nombre es requerido", campo="nombre")
    except ValidacionError as e:
        print(f"[OK] ValidacionError: {e.to_dict()}")
    
    # Test 2: AlumnoNoEncontrado
    try:
        raise AlumnoNoEncontrado("123-456")
    except AlumnoNoEncontrado as e:
        print(f"[OK] AlumnoNoEncontrado: {e.to_dict()}")
    
    # Test 3: DNIDuplicado
    try:
        raise DNIDuplicado("12345678")
    except DNIDuplicado as e:
        print(f"[OK] DNIDuplicado: {e.to_dict()}")
    
    # Test 4: SessionExpiredError
    try:
        raise SessionExpiredError()
    except SessionExpiredError as e:
        print(f"[OK] SessionExpiredError: {e.to_dict()}")
    
    # Test 5: Capturar todas con clase base
    try:
        raise RepositoryError("Conexion fallida")
    except DomainException as e:
        print(f"[OK] DomainException base: {e.to_dict()}")
    
    print("\n=== Todas las pruebas pasaron ===")
