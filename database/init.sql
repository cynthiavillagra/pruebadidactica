-- ═══════════════════════════════════════════════════════════════════════════
-- SCRIPT DE INICIALIZACIÓN DE BASE DE DATOS
-- Proyecto: App Didáctica CRUD de Alumnos
-- Base de Datos: Supabase (PostgreSQL 15+)
-- Versión: 1.0.0
-- Fecha: 2025-12-22
-- ═══════════════════════════════════════════════════════════════════════════
--
-- INSTRUCCIONES DE USO:
-- 1. Acceder al panel de Supabase: https://app.supabase.com
-- 2. Seleccionar el proyecto
-- 3. Ir a SQL Editor (icono de base de datos)
-- 4. Crear un nuevo query
-- 5. Copiar y pegar este script completo
-- 6. Ejecutar (Run / Cmd+Enter)
--
-- ADVERTENCIA:
-- Este script es IDEMPOTENTE (puede ejecutarse múltiples veces sin errores)
-- gracias al uso de IF NOT EXISTS y DROP IF EXISTS.
--
-- ═══════════════════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 1: EXTENSIONES
-- ═══════════════════════════════════════════════════════════════════════════

-- Extensión para generar UUIDs (ya viene habilitada en Supabase por defecto)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Nota: En Supabase, gen_random_uuid() está disponible sin necesidad de extensión


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 2: TABLA PRINCIPAL - ALUMNOS
-- ═══════════════════════════════════════════════════════════════════════════

-- POR QUÉ UUID COMO ID:
-- - No expone la cantidad de registros (a diferencia de autoincrement)
-- - Funciona en sistemas distribuidos sin colisiones
-- - Más seguro (no predecible)

-- POR QUÉ TIMESTAMPTZ (TIMESTAMP WITH TIME ZONE):
-- - Almacena la fecha en UTC internamente
-- - Evita problemas de zonas horarias
-- - Supabase convierte automáticamente a la zona del cliente

CREATE TABLE IF NOT EXISTS alumnos (
    -- ─────────────────────────────────────────────────────────────────────────
    -- Clave primaria: UUID generado automáticamente
    -- ─────────────────────────────────────────────────────────────────────────
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- ─────────────────────────────────────────────────────────────────────────
    -- Datos del alumno
    -- ─────────────────────────────────────────────────────────────────────────
    -- POR QUÉ VARCHAR(100): Balance entre flexibilidad y límite razonable
    -- Nombres muy largos son raros; 100 chars cubre casos extremos
    nombre VARCHAR(100) NOT NULL 
        CONSTRAINT chk_nombre_no_vacio CHECK (LENGTH(TRIM(nombre)) > 0),
    
    apellido VARCHAR(100) NOT NULL 
        CONSTRAINT chk_apellido_no_vacio CHECK (LENGTH(TRIM(apellido)) > 0),
    
    -- ─────────────────────────────────────────────────────────────────────────
    -- DNI: Identificador único del alumno
    -- ─────────────────────────────────────────────────────────────────────────
    -- POR QUÉ VARCHAR(20): Permite diferentes formatos internacionales
    -- Argentina: 8 dígitos, España: 8 dígitos + letra, etc.
    -- POR QUÉ UNIQUE: Requisito de negocio RF-005 (DNI no puede repetirse)
    dni VARCHAR(20) NOT NULL UNIQUE 
        CONSTRAINT chk_dni_no_vacio CHECK (LENGTH(TRIM(dni)) > 0),
    
    -- ─────────────────────────────────────────────────────────────────────────
    -- Timestamps de auditoría
    -- ─────────────────────────────────────────────────────────────────────────
    -- POR QUÉ DEFAULT NOW(): Automático, menos errores humanos
    -- POR QUÉ NOT NULL: Siempre queremos saber cuándo se creó/modificó
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Comentarios de documentación (visibles en el schema de Supabase)
COMMENT ON TABLE alumnos IS 
    'Tabla principal que almacena datos de estudiantes. Parte del MVP CRUD didáctico.';
COMMENT ON COLUMN alumnos.id IS 
    'Identificador único UUID v4, generado automáticamente por gen_random_uuid().';
COMMENT ON COLUMN alumnos.nombre IS 
    'Nombre del alumno. Requerido. Máximo 100 caracteres. No puede estar vacío.';
COMMENT ON COLUMN alumnos.apellido IS 
    'Apellido del alumno. Requerido. Máximo 100 caracteres. No puede estar vacío.';
COMMENT ON COLUMN alumnos.dni IS 
    'Documento Nacional de Identidad. Único en todo el sistema. No puede estar vacío.';
COMMENT ON COLUMN alumnos.created_at IS 
    'Timestamp de creación del registro (UTC). Se genera automáticamente.';
COMMENT ON COLUMN alumnos.updated_at IS 
    'Timestamp de última modificación (UTC). Se actualiza con trigger.';


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 3: ÍNDICES
-- ═══════════════════════════════════════════════════════════════════════════

-- POR QUÉ ÍNDICES:
-- - Mejoran la velocidad de búsqueda
-- - El índice de DNI ya existe implícitamente por UNIQUE
-- - Los otros índices optimizan casos de uso comunes

-- Índice para ordenar por apellido (caso de uso más común: listar alumnos)
CREATE INDEX IF NOT EXISTS idx_alumnos_apellido 
    ON alumnos(apellido);

-- Índice compuesto para búsqueda por nombre completo
CREATE INDEX IF NOT EXISTS idx_alumnos_apellido_nombre 
    ON alumnos(apellido, nombre);

-- Índice para búsquedas case-insensitive (futuro: buscador)
CREATE INDEX IF NOT EXISTS idx_alumnos_apellido_lower 
    ON alumnos(LOWER(apellido));


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 4: FUNCIÓN Y TRIGGER PARA updated_at
-- ═══════════════════════════════════════════════════════════════════════════

-- POR QUÉ TRIGGER Y NO LÓGICA EN APLICACIÓN:
-- - Garantiza que SIEMPRE se actualiza, sin depender del código
-- - Centralizado: un solo lugar para la lógica
-- - Funciona aunque se modifique directamente en SQL

-- Función reutilizable para cualquier tabla
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualiza el timestamp solo si realmente cambió algún dato
    -- POR QUÉ NOW(): Supabase maneja UTC internamente
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Comentario en la función
COMMENT ON FUNCTION trigger_set_updated_at() IS 
    'Función de trigger que actualiza automáticamente el campo updated_at.';

-- Eliminar trigger si existe (para idempotencia)
DROP TRIGGER IF EXISTS trigger_alumnos_updated_at ON alumnos;

-- Crear trigger que ejecuta antes de cada UPDATE
CREATE TRIGGER trigger_alumnos_updated_at
    BEFORE UPDATE ON alumnos
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_updated_at();


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 5: ROW LEVEL SECURITY (RLS)
-- ═══════════════════════════════════════════════════════════════════════════

-- POR QUÉ RLS:
-- - Seguridad a nivel de base de datos
-- - Aunque alguien obtenga la API key, solo puede hacer lo permitido
-- - Supabase lo requiere para usar la anon key de forma segura

-- Habilitar RLS en la tabla (OBLIGATORIO en Supabase para seguridad)
ALTER TABLE alumnos ENABLE ROW LEVEL SECURITY;

-- ─────────────────────────────────────────────────────────────────────────
-- Políticas para usuarios AUTENTICADOS
-- ─────────────────────────────────────────────────────────────────────────

-- POR QUÉ 'authenticated' Y NO 'anon':
-- - Solo usuarios logueados pueden ver/modificar datos
-- - Previene acceso anónimo a la información

-- Política: SELECT (Leer)
CREATE POLICY "Usuarios autenticados pueden leer alumnos"
    ON alumnos
    FOR SELECT
    TO authenticated
    USING (true);

-- Política: INSERT (Crear)
CREATE POLICY "Usuarios autenticados pueden crear alumnos"
    ON alumnos
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Política: UPDATE (Actualizar)
CREATE POLICY "Usuarios autenticados pueden actualizar alumnos"
    ON alumnos
    FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Política: DELETE (Eliminar)
CREATE POLICY "Usuarios autenticados pueden eliminar alumnos"
    ON alumnos
    FOR DELETE
    TO authenticated
    USING (true);


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 6: DATOS DE PRUEBA (OPCIONAL - SOLO DESARROLLO)
-- ═══════════════════════════════════════════════════════════════════════════

-- ADVERTENCIA: Comentar o eliminar en producción
-- Estos datos son útiles para probar la aplicación sin tener que crear alumnos manualmente

-- Descomentar las siguientes líneas para insertar datos de prueba:

/*
INSERT INTO alumnos (nombre, apellido, dni) VALUES
    ('Juan', 'Pérez', '12345678'),
    ('María', 'González', '23456789'),
    ('Carlos', 'López', '34567890'),
    ('Ana', 'Martínez', '45678901'),
    ('Luis', 'García', '56789012')
ON CONFLICT (dni) DO NOTHING;  -- Evita errores si ya existen
*/


-- ═══════════════════════════════════════════════════════════════════════════
-- SECCIÓN 7: VERIFICACIÓN
-- ═══════════════════════════════════════════════════════════════════════════

-- Verificar que la tabla se creó correctamente
-- SELECT * FROM alumnos LIMIT 5;

-- Verificar las políticas RLS
-- SELECT * FROM pg_policies WHERE tablename = 'alumnos';

-- Verificar los índices
-- SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'alumnos';

-- Verificar el trigger
-- SELECT trigger_name, event_manipulation, action_statement 
-- FROM information_schema.triggers 
-- WHERE event_object_table = 'alumnos';


-- ═══════════════════════════════════════════════════════════════════════════
-- FIN DEL SCRIPT
-- ═══════════════════════════════════════════════════════════════════════════

-- Mensaje de confirmación (se mostrará en los logs)
DO $$
BEGIN
    RAISE NOTICE '✅ Script de inicialización ejecutado exitosamente';
    RAISE NOTICE '📊 Tabla "alumnos" creada/verificada';
    RAISE NOTICE '🔒 Row Level Security habilitado';
    RAISE NOTICE '⚡ Trigger de updated_at configurado';
END $$;
