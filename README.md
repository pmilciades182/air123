# Airflow - Proyecto de Orquestación de Tareas

Proyecto de Apache Airflow dockerizado para la ejecución de tareas programadas. **Soporta múltiples instancias** en el mismo servidor.

## Descripción

Este proyecto implementa Apache Airflow 3.1.3 usando Docker, conectado a una base de datos PostgreSQL 14 para almacenar metadata. El proyecto está completamente parametrizado mediante variables de entorno, permitiendo ejecutar múltiples instancias independientes en el mismo servidor.

## Características

✅ Apache Airflow 3.1.3 (última versión estable)
✅ Python 3.13
✅ PostgreSQL 14 como base de datos de metadata
✅ LocalExecutor para ejecución de tareas
✅ Soporte para múltiples instancias en el mismo servidor
✅ Configuración completamente parametrizable
✅ Flujo de trabajo para edición local de DAGs

## Requisitos Previos

- Docker y Docker Compose instalados
- Acceso a PostgreSQL 14 (servidor: `192.168.24.109:5433`)
- Usuario y base de datos creados en PostgreSQL para cada instancia

## Estructura del Proyecto

```
airflow_develop/
├── docker/
│   ├── Dockerfile              # Imagen personalizada de Airflow 3.1.3
│   └── requirements.txt        # Dependencias Python adicionales
├── dags_local/                 # DAGs editables localmente (versionado en Git)
│   └── ejemplo_dag.py          # DAG de ejemplo
├── dags/                       # DAGs desplegados (generado, NO versionado)
├── logs/                       # Logs de Airflow (generado automáticamente)
├── plugins/                    # Plugins personalizados de Airflow
├── docker-compose.yml          # Configuración de servicios Docker
├── Makefile                    # Comandos para gestionar el proyecto
├── .env                        # Variables de entorno de la instancia actual
├── .env.example                # Plantilla de configuración
├── .env.instance2.example      # Ejemplo para segunda instancia
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
```

## Configuración de Variables de Entorno

El proyecto usa un archivo `.env` para toda la configuración. Las variables principales son:

### Variables Obligatorias

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `PROJECT_NAME` | Nombre único de la instancia | `airflow1` |
| `POSTGRES_HOST` | Servidor PostgreSQL | `192.168.24.109` |
| `POSTGRES_PORT` | Puerto PostgreSQL | `5433` |
| `POSTGRES_DB` | Base de datos (única por instancia) | `airflow_db_instance1` |
| `POSTGRES_USER` | Usuario de BD (único por instancia) | `airflow_user_instance1` |
| `POSTGRES_PASSWORD` | Contraseña de BD | `airflow2025_instance1` |
| `AIRFLOW_WEBSERVER_PORT` | Puerto web (único por instancia) | `4000` |
| `AIRFLOW_FERNET_KEY` | Clave de encriptación (única) | Generar con comando |
| `AIRFLOW_JWT_SECRET` | Secret JWT (único) | Generar con comando |
| `AIRFLOW_INTERNAL_API_SECRET` | Secret API interna (único) | String único |

### Generar Claves de Seguridad

```bash
# Generar AIRFLOW_FERNET_KEY
docker run --rm apache/airflow:3.1.3-python3.13 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generar AIRFLOW_JWT_SECRET
openssl rand -base64 16
```

## Inicio Rápido - Primera Instancia

### 1. Configurar Variables de Entorno

```bash
# Copiar el ejemplo y editar
cp .env.example .env
nano .env
```

Ajusta los valores en `.env`:
```bash
PROJECT_NAME=airflow1
POSTGRES_DB=airflow_db
POSTGRES_USER=airflow_user
POSTGRES_PASSWORD=airflow2025
AIRFLOW_WEBSERVER_PORT=4000
# ... generar y configurar las claves de seguridad
```

### 2. Crear Base de Datos en PostgreSQL

Conéctate a PostgreSQL y ejecuta:

```sql
CREATE USER airflow_user WITH PASSWORD 'airflow2025';
CREATE DATABASE airflow_db OWNER airflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
```

### 3. Construir e Iniciar

```bash
make build
make start
```

### 4. Acceder a Airflow UI

Abre tu navegador en: http://localhost:4000

**Credenciales:**
- Usuario: `airflow`
- Contraseña: Ejecuta `make get-password` para obtenerla

### 5. Desplegar el DAG de Ejemplo

```bash
make deploy
```

## Múltiples Instancias en el Mismo Servidor

El proyecto está diseñado para soportar múltiples instancias de Airflow corriendo simultáneamente en el mismo servidor. Cada instancia es completamente independiente.

### Requisitos para Múltiples Instancias

Cada instancia **DEBE** tener:
- ✅ Un `PROJECT_NAME` único
- ✅ Un puerto `AIRFLOW_WEBSERVER_PORT` único
- ✅ Una base de datos PostgreSQL separada
- ✅ Claves de seguridad únicas (Fernet, JWT, Internal API)
- ✅ Su propio directorio en el servidor

### Pasos para Crear una Segunda Instancia

#### 1. Copiar el Proyecto

```bash
# En el servidor, copia el proyecto a un nuevo directorio
cp -r /home/paxo/airflow_develop /home/paxo/airflow_develop_2
cd /home/paxo/airflow_develop_2
```

#### 2. Configurar el .env de la Segunda Instancia

```bash
# Usa el ejemplo de segunda instancia como base
cp .env.instance2.example .env
nano .env
```

Configura los valores únicos:

```bash
PROJECT_NAME=airflow2
POSTGRES_DB=airflow_db_instance2
POSTGRES_USER=airflow_user_instance2
POSTGRES_PASSWORD=airflow2025_instance2
AIRFLOW_WEBSERVER_PORT=4001
```

**IMPORTANTE**: Genera **nuevas claves únicas** para esta instancia:

```bash
# Generar nueva FERNET_KEY
docker run --rm apache/airflow:3.1.3-python3.13 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generar nuevo JWT_SECRET
openssl rand -base64 16
```

#### 3. Crear Base de Datos en PostgreSQL

```sql
CREATE USER airflow_user_instance2 WITH PASSWORD 'airflow2025_instance2';
CREATE DATABASE airflow_db_instance2 OWNER airflow_user_instance2;
GRANT ALL PRIVILEGES ON DATABASE airflow_db_instance2 TO airflow_user_instance2;
```

#### 4. Construir e Iniciar la Segunda Instancia

```bash
cd /home/paxo/airflow_develop_2
make build
make start
```

#### 5. Acceder a las Instancias

- **Instancia 1**: http://localhost:4000
- **Instancia 2**: http://localhost:4001
- **Instancia 3**: http://localhost:4002 (si existe)

### Gestionar Múltiples Instancias

Cada instancia se gestiona de forma independiente desde su propio directorio:

```bash
# Instancia 1
cd /home/paxo/airflow_develop
make status      # Ver estado de la instancia 1
make logs        # Ver logs de la instancia 1

# Instancia 2
cd /home/paxo/airflow_develop_2
make status      # Ver estado de la instancia 2
make logs        # Ver logs de la instancia 2
```

### Tabla de Referencia para Múltiples Instancias

| Instancia | Directorio | PROJECT_NAME | Puerto | Base de Datos |
|-----------|-----------|--------------|--------|---------------|
| 1 | `/home/paxo/airflow_develop` | `airflow1` | 4000 | `airflow_db` |
| 2 | `/home/paxo/airflow_develop_2` | `airflow2` | 4001 | `airflow_db_instance2` |
| 3 | `/home/paxo/airflow_develop_3` | `airflow3` | 4002 | `airflow_db_instance3` |

## Comandos Disponibles (Makefile)

Todos los comandos se ejecutan dentro del directorio de la instancia correspondiente.

### Comandos Principales

```bash
# Ver ayuda (muestra la instancia actual)
make help

# Construir las imágenes de Docker
make build

# Iniciar Airflow (webserver + scheduler + triggerer + dag-processor)
make start

# Detener todos los contenedores
make stop

# Reiniciar Airflow
make restart
```

### Comandos de Despliegue de DAGs

```bash
# Desplegar todos los DAGs de dags_local/ a dags/
make deploy

# Desplegar solo un archivo específico
make deploy FILE=mi_dag.py
```

### Comandos de Monitoreo

```bash
# Ver logs de todos los servicios
make logs

# Ver logs solo del webserver
make logs-webserver

# Ver logs solo del scheduler
make logs-scheduler

# Ver estado de los contenedores
make status

# Obtener contraseña de acceso web
make get-password
```

### Comandos de Limpieza

```bash
# Limpiar contenedores y volúmenes
make clean
```

## Flujo de Trabajo para DAGs

### Por qué `dags_local/` y `dags/`?

- **`dags_local/`**: Archivos con permisos de tu usuario, editables en VSCode/IDE
- **`dags/`**: Carpeta montada en Docker (permisos de contenedor)

### Crear un Nuevo DAG

1. **Crear el archivo en `dags_local/`**:

```bash
# Opción 1: Copiar el ejemplo
cp dags_local/ejemplo_dag.py dags_local/mi_nuevo_dag.py

# Opción 2: Crear desde cero
nano dags_local/mi_nuevo_dag.py
```

2. **Editar el DAG en tu IDE favorito**

3. **Desplegar a Airflow**:

```bash
# Desplegar solo este archivo
make deploy FILE=mi_nuevo_dag.py

# O desplegar todos
make deploy
```

4. **Verificar en Airflow UI** - El DAG aparecerá en ~30 segundos

### Editar un DAG Existente

1. Editar el archivo en `dags_local/`
2. Guardar cambios
3. Redesplegar: `make deploy FILE=mi_dag.py`
4. Airflow detectará los cambios automáticamente

## Servicios Docker

El proyecto levanta los siguientes servicios:

- **airflow-webserver**: Interfaz web y API server (puerto configurable)
- **airflow-scheduler**: Programador de tareas
- **airflow-triggerer**: Gestor de tareas asíncronas (requerido en Airflow 3.x)
- **airflow-dag-processor**: Procesador de DAGs (requerido en Airflow 3.x)
- **airflow-init**: Inicialización y migraciones de BD (se ejecuta una vez)

## Solución de Problemas

### Problema: Contenedores no inician

```bash
# Ver logs para identificar el error
make logs

# Verificar estado de contenedores
make status
```

### Problema: Conflicto de puertos

Si obtienes un error de puerto en uso:

1. Verifica qué está usando el puerto: `netstat -tuln | grep 4000`
2. Cambia `AIRFLOW_WEBSERVER_PORT` en `.env` a un puerto disponible
3. Reinicia: `make restart`

### Problema: DAGs no aparecen en la UI

1. Verifica que el archivo esté en `dags/`: `ls -la dags/`
2. Revisa errores de sintaxis Python
3. Espera unos segundos (Airflow escanea cada 30 segundos)
4. Revisa los logs: `make logs-scheduler`

### Problema: Tareas fallan con "Invalid auth token"

Este error ocurre cuando las claves de seguridad no están configuradas correctamente:

1. Asegúrate de que `AIRFLOW_JWT_SECRET` esté configurado en `.env`
2. Asegúrate de que `AIRFLOW_FERNET_KEY` esté configurado en `.env`
3. Reinicia los servicios: `make restart`

### Problema: No puedo conectar a PostgreSQL

Verifica:
1. El servidor PostgreSQL esté accesible: `telnet 192.168.24.109 5433`
2. Las credenciales en `.env` sean correctas
3. El firewall permita la conexión al puerto 5433
4. El usuario y base de datos existan en PostgreSQL

### Problema: Conflicto entre instancias

Si dos instancias usan el mismo `PROJECT_NAME`:

1. Detén ambas instancias
2. Asegúrate de que cada `.env` tenga un `PROJECT_NAME` único
3. Reinicia cada instancia desde su directorio

## Versiones

- **Apache Airflow**: 3.1.3
- **Python**: 3.13
- **PostgreSQL**: 14
- **Executor**: LocalExecutor

## Notas Importantes

- **DAGs**: Edita en `dags_local/` (versionado en Git), despliega con `make deploy`
- **Logs**: Se almacenan en la carpeta `logs/` (no versionado)
- **Plugins**: Los plugins personalizados van en `plugins/`
- **Credenciales**: El archivo `.env` NO debe versionarse en Git
- **Metadata**: Se almacena en PostgreSQL 14
- **Carpeta dags/**: NO versionada, se genera automáticamente con `make deploy`
- **Múltiples instancias**: Cada instancia DEBE tener su propio `PROJECT_NAME`, puerto, y base de datos

## Conexiones y DAGs de Ejemplo

Este proyecto incluye conexiones preconfiguradas y DAGs de ejemplo listos para usar:

### Conexiones Disponibles

- **SMTP** (`smtp_idesa`) - Envío de correos electrónicos
- **PostgreSQL** (`postgres_idesa`) - Base de datos planos
- **IBM i DB2** (`ibmi_dev`) - AS/400 con driver ODBC

### DAGs de Ejemplo

- `dag_email_manual.py` - Envío de email de prueba
- `dag_postgres_test.py` - Consulta a tabla FRACCION en PostgreSQL
- `dag_ibmi_test.py` - Consulta a tabla ubitfra en IBM i DB2

**📖 Ver documentación completa:** [docs/](docs/)

## Documentación

**📚 [DOCUMENTATION.md](DOCUMENTATION.md)** - Índice visual completo de toda la documentación

### Guías Principales

- **[📖 docs/README.md](docs/README.md)** - Índice detallado de documentación técnica
- **[🚀 Installation Guide](docs/installation-guide.md)** - Configuración inicial y setup
- **[🔌 Connections Configuration](docs/connections-configuration.md)** - Configuración de conexiones
- **[📝 DAG Development Guide](docs/dag-development-guide.md)** - Desarrollo de DAGs
- **[🔧 IBM i ODBC Driver Setup](docs/ibmi-odbc-driver-setup.md)** - Setup del driver ODBC

### Recursos Externos

- [Documentación oficial de Airflow 3.x](https://airflow.apache.org/docs/apache-airflow/3.1.3/)
- [Guía de DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Operadores disponibles](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)
- [Airflow 3.0 Migration Guide](https://airflow.apache.org/docs/apache-airflow/3.1.3/migrations-ref.html)

## Arquitectura de Airflow 3.x

Airflow 3.x introduce cambios arquitectónicos significativos:

1. **API Server**: El webserver ahora usa `api-server` en lugar de `webserver`
2. **Execution API**: Nueva API para ejecución de tareas que requiere autenticación JWT
3. **DAG Processor**: Servicio separado para procesar archivos de DAGs
4. **Triggerer**: Servicio para manejar tareas asíncronas (deferrable)
5. **Simple Auth Manager**: Nuevo sistema de autenticación (reemplaza Flask-AppBuilder)

Todos estos componentes están configurados y funcionando en este proyecto.
