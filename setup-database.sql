-- ==============================================================================
-- Script SQL para crear base de datos y usuario de Airflow
-- ==============================================================================
-- Este script crea un usuario y base de datos para Airflow
--
-- INSTRUCCIONES:
-- 1. Ajusta los valores de usuario, contraseña y base de datos según tu .env
-- 2. Conéctate a PostgreSQL como superusuario:
--    psql -U postgres -h 192.168.24.109 -p 5433
-- 3. Ejecuta este script:
--    \i setup-database.sql
-- 4. O ejecuta línea por línea copiando y pegando
-- ==============================================================================

-- ==============================================================================
-- CONFIGURACIÓN PARA DESARROLLO LOCAL
-- ==============================================================================
-- Descomenta y ajusta estos valores para desarrollo local

-- CREATE USER airflow_local_user WITH PASSWORD 'airflow_local_pass_2025';
-- CREATE DATABASE airflow_local_db OWNER airflow_local_user;
-- GRANT ALL PRIVILEGES ON DATABASE airflow_local_db TO airflow_local_user;

-- ==============================================================================
-- CONFIGURACIÓN PARA INSTANCIA 1 (Producción/Servidor)
-- ==============================================================================
-- Usuario y base de datos para la primera instancia

CREATE USER airflow_user WITH PASSWORD 'airflow2025';
CREATE DATABASE airflow_db OWNER airflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

-- ==============================================================================
-- CONFIGURACIÓN PARA INSTANCIA 2 (Producción/Servidor)
-- ==============================================================================
-- Descomenta para crear una segunda instancia

-- CREATE USER airflow_user_instance2 WITH PASSWORD 'airflow2025_instance2';
-- CREATE DATABASE airflow_db_instance2 OWNER airflow_user_instance2;
-- GRANT ALL PRIVILEGES ON DATABASE airflow_db_instance2 TO airflow_user_instance2;

-- ==============================================================================
-- CONFIGURACIÓN PARA INSTANCIA 3 (Producción/Servidor)
-- ==============================================================================
-- Descomenta para crear una tercera instancia

-- CREATE USER airflow_user_instance3 WITH PASSWORD 'airflow2025_instance3';
-- CREATE DATABASE airflow_db_instance3 OWNER airflow_user_instance3;
-- GRANT ALL PRIVILEGES ON DATABASE airflow_db_instance3 TO airflow_user_instance3;

-- ==============================================================================
-- VERIFICACIÓN
-- ==============================================================================
-- Comandos para verificar que todo se creó correctamente

-- Listar todas las bases de datos:
-- \l

-- Listar todos los usuarios:
-- \du

-- Conectarse a la base de datos creada:
-- \c airflow_db

-- Ver permisos del usuario:
-- \dp

-- ==============================================================================
-- COMANDOS ÚTILES
-- ==============================================================================
--
-- Conectarse a PostgreSQL remotamente:
--   psql -U postgres -h 192.168.24.109 -p 5433
--
-- Conectarse a PostgreSQL localmente:
--   psql -U postgres
--
-- Eliminar base de datos y usuario (si necesitas empezar de nuevo):
--   DROP DATABASE airflow_db;
--   DROP USER airflow_user;
--
-- Ver conexiones activas a una base de datos:
--   SELECT * FROM pg_stat_activity WHERE datname = 'airflow_db';
--
-- Terminar todas las conexiones a una base de datos:
--   SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'airflow_db';
--
-- ==============================================================================
