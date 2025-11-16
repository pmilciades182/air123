# Guía Rápida de Configuración de Airflow

Esta es una guía rápida para configurar una nueva instancia de Airflow desde cero.

## Opción 1: Configuración Rápida con Script Automático ⚡

```bash
# 1. Generar claves de seguridad automáticamente
./generate-keys.sh

# 2. Editar .env y ajustar la configuración de PostgreSQL
nano .env

# 3. Crear la base de datos en PostgreSQL
psql -U postgres -h TU_HOST -p TU_PUERTO < setup-database.sql

# 4. Construir e iniciar Airflow
make build
make start

# 5. Obtener contraseña de acceso
make get-password

# 6. Acceder a la UI
# http://localhost:PUERTO (el puerto configurado en AIRFLOW_WEBSERVER_PORT)
```

## Opción 2: Configuración Manual Paso a Paso 🔧

### Paso 1: Crear archivo .env

Elige una de estas opciones según tu entorno:

**Para desarrollo local:**
```bash
cp .env.example.local .env
```

**Para servidor/producción:**
```bash
cp .env.example .env
```

**Para segunda instancia:**
```bash
cp .env.instance2.example .env
```

### Paso 2: Generar Claves de Seguridad

**Generar AIRFLOW_FERNET_KEY:**
```bash
docker run --rm apache/airflow:3.1.3-python3.13 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**Generar AIRFLOW_JWT_SECRET:**
```bash
openssl rand -base64 16
```

### Paso 3: Editar .env

Abre el archivo `.env` y configura las siguientes variables:

```bash
# Identificación única de la instancia
PROJECT_NAME=airflow1              # Cambia para cada instancia

# PostgreSQL
POSTGRES_HOST=192.168.24.109       # Tu servidor PostgreSQL
POSTGRES_PORT=5433                 # Puerto de PostgreSQL
POSTGRES_DB=airflow_db             # Nombre de la base de datos
POSTGRES_USER=airflow_user         # Usuario de PostgreSQL
POSTGRES_PASSWORD=airflow2025      # Contraseña de PostgreSQL

# Puerto del webserver
AIRFLOW_WEBSERVER_PORT=4000        # Puerto único por instancia

# Claves de seguridad (pegar las generadas en paso 2)
AIRFLOW_FERNET_KEY=TU_CLAVE_FERNET
AIRFLOW_JWT_SECRET=TU_JWT_SECRET
AIRFLOW_INTERNAL_API_SECRET=un-secret-unico

# Usuario web
AIRFLOW_WWW_USER_USERNAME=airflow
AIRFLOW_WWW_USER_PASSWORD=airflow
```

### Paso 4: Crear Base de Datos en PostgreSQL

**Conectarse a PostgreSQL:**
```bash
psql -U postgres -h 192.168.24.109 -p 5433
```

**Ejecutar comandos SQL:**
```sql
CREATE USER airflow_user WITH PASSWORD 'airflow2025';
CREATE DATABASE airflow_db OWNER airflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
\q
```

O usar el script SQL:
```bash
psql -U postgres -h 192.168.24.109 -p 5433 < setup-database.sql
```

### Paso 5: Construir e Iniciar Airflow

```bash
# Construir las imágenes Docker
make build

# Iniciar todos los servicios
make start

# Ver el estado
make status

# Ver logs
make logs
```

### Paso 6: Acceder a Airflow

**Obtener contraseña:**
```bash
make get-password
```

**Acceder a la UI:**
- URL: http://localhost:PUERTO (el puerto configurado en .env)
- Usuario: El configurado en `AIRFLOW_WWW_USER_USERNAME`
- Contraseña: La obtenida con `make get-password`

### Paso 7: Desplegar DAGs

```bash
# Desplegar todos los DAGs de dags_local/
make deploy

# O desplegar un DAG específico
make deploy FILE=mi_dag.py
```

## Configuración para Múltiples Instancias

### Tabla de Valores para Cada Instancia

| Variable | Instancia 1 | Instancia 2 | Instancia 3 |
|----------|-------------|-------------|-------------|
| `PROJECT_NAME` | `airflow1` | `airflow2` | `airflow3` |
| `AIRFLOW_WEBSERVER_PORT` | `4000` | `4001` | `4002` |
| `POSTGRES_DB` | `airflow_db` | `airflow_db_instance2` | `airflow_db_instance3` |
| `POSTGRES_USER` | `airflow_user` | `airflow_user_instance2` | `airflow_user_instance3` |

### Crear Segunda Instancia

```bash
# 1. Copiar el proyecto completo
cp -r /home/paxo/airflow_develop /home/paxo/airflow_develop_2
cd /home/paxo/airflow_develop_2

# 2. Configurar .env con valores únicos
cp .env.instance2.example .env
./generate-keys.sh  # Generar nuevas claves únicas

# 3. Crear nueva base de datos en PostgreSQL
# (Ajustar los valores en setup-database.sql primero)

# 4. Iniciar
make build
make start
```

## Comandos Útiles

```bash
# Ver ayuda (muestra la instancia actual)
make help

# Ver estado de contenedores
make status

# Ver logs en tiempo real
make logs

# Ver logs de un servicio específico
make logs-webserver
make logs-scheduler

# Reiniciar todo
make restart

# Detener todo
make stop

# Limpiar todo (incluye volúmenes y base de datos local)
make clean

# Obtener contraseña
make get-password
```

## Verificación de la Instalación

**1. Verificar que todos los servicios estén corriendo:**
```bash
make status
```

Deberías ver estos servicios `Up`:
- airflow-webserver
- airflow-scheduler
- airflow-triggerer
- airflow-dag-processor

**2. Verificar logs sin errores:**
```bash
make logs-scheduler | grep -i error
```

**3. Acceder a la UI y verificar:**
- Panel de salud (Health) - todos los componentes en verde
- DAGs - debería aparecer `ejemplo_dag`

## Solución de Problemas Comunes

### Error: Puerto en uso
```bash
# Cambiar AIRFLOW_WEBSERVER_PORT en .env a otro puerto
nano .env
make restart
```

### Error: No puede conectar a PostgreSQL
```bash
# Verificar conectividad
telnet 192.168.24.109 5433

# Verificar credenciales en .env
cat .env | grep POSTGRES
```

### Error: Invalid auth token
```bash
# Verificar que las claves estén configuradas
cat .env | grep -E "(FERNET|JWT|SECRET)"

# Regenerar claves si es necesario
./generate-keys.sh
make restart
```

### DAGs no aparecen
```bash
# Verificar que el archivo esté en dags/
ls -la dags/

# Redesplegar
make deploy

# Ver logs del dag-processor
docker-compose --project-name $(grep PROJECT_NAME .env | cut -d= -f2) logs airflow-dag-processor
```

## Archivos de Configuración

| Archivo | Descripción |
|---------|-------------|
| `.env` | Configuración de la instancia (NO versionar) |
| `.env.example` | Plantilla para servidor/producción |
| `.env.example.local` | Plantilla para desarrollo local |
| `.env.instance2.example` | Ejemplo para segunda instancia |
| `generate-keys.sh` | Script para generar claves automáticamente |
| `setup-database.sql` | Script SQL para crear base de datos |
| `docker-compose.yml` | Configuración de servicios Docker |
| `Makefile` | Comandos de gestión |

## Recursos Adicionales

- [README completo](README.md) - Documentación completa del proyecto
- [Documentación oficial de Airflow 3.x](https://airflow.apache.org/docs/apache-airflow/3.1.3/)
- [Guía de DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
