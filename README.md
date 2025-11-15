# Airflow - Proyecto de Orquestación de Tareas

Proyecto de Apache Airflow dockerizado para la ejecución de tareas programadas.

## Descripción

Este proyecto implementa Apache Airflow usando Docker, conectado a una base de datos PostgreSQL 14 para almacenar metadata. El webserver está configurado para ejecutarse en el puerto **4000**.

## Requisitos Previos

- Docker y Docker Compose instalados
- Acceso a PostgreSQL 14 (servidor: `192.168.24.109:5433`)
- Usuario y base de datos creados en PostgreSQL

## Configuración de Base de Datos

### Credenciales PostgreSQL

**Servidor PostgreSQL 14:**
- Host: `192.168.24.109`
- Puerto: `5433`
- Base de datos: `airflow_db`
- Usuario Airflow: `airflow_user`
- Contraseña: `airflow2025`

**Credenciales Superusuario (solo para administración):**
- Usuario: `postgres`
- Contraseña: `5PASzT0@iB`

### Usuario y Base de Datos ya creados

Ya se ejecutaron los siguientes comandos en PostgreSQL 14:

```sql
CREATE USER airflow_user WITH PASSWORD 'airflow2025';
CREATE DATABASE airflow_db OWNER airflow_user;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
```

## Estructura del Proyecto

```
airflow_develop/
├── docker/
│   ├── Dockerfile              # Imagen personalizada de Airflow
│   └── requirements.txt        # Dependencias Python adicionales
├── dags/
│   └── ejemplo_dag.py          # DAG de ejemplo
├── logs/                       # Logs de Airflow (generado automáticamente)
├── plugins/                    # Plugins personalizados de Airflow
├── docker-compose.yml          # Configuración de servicios Docker
├── Makefile                    # Comandos para gestionar el proyecto
├── .env                        # Variables de entorno (NO versionar)
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
```

## Comandos Disponibles (Makefile)

### Comandos Principales

```bash
# Ver ayuda
make help

# Construir las imágenes de Docker
make build

# Iniciar Airflow (webserver + scheduler)
make start

# Detener todos los contenedores
make stop

# Reiniciar Airflow
make restart
```

### Comandos Adicionales

```bash
# Ver logs de todos los servicios
make logs

# Ver logs solo del webserver
make logs-webserver

# Ver logs solo del scheduler
make logs-scheduler

# Ver estado de los contenedores
make status

# Limpiar contenedores y volúmenes
make clean

# Inicializar estructura de carpetas
make init
```

## Inicio Rápido

### 1. Primera vez - Construir e Iniciar

```bash
make build
make start
```

### 2. Acceder a Airflow UI

Abre tu navegador en: http://localhost:4000

**Credenciales de acceso:**
- Usuario: `airflow`
- Contraseña: `airflow`

### 3. Verificar el DAG de ejemplo

En la interfaz de Airflow verás el DAG `ejemplo_dag` que:
- Se ejecuta diariamente a las 8:00 AM
- Contiene 4 tareas de ejemplo
- Muestra un flujo básico de trabajo

## Crear Nuevos DAGs

1. Crea un archivo Python en la carpeta `dags/`
2. Define tu DAG siguiendo la estructura del ejemplo
3. El DAG aparecerá automáticamente en la UI de Airflow

Ejemplo mínimo:

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def mi_funcion():
    print("Hola desde Airflow!")

with DAG(
    'mi_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    tarea = PythonOperator(
        task_id='mi_tarea',
        python_callable=mi_funcion,
    )
```

## Servicios Docker

El proyecto levanta los siguientes servicios:

- **airflow-webserver**: Interfaz web (puerto 4000)
- **airflow-scheduler**: Programador de tareas
- **airflow-init**: Inicialización y migraciones de BD

## Gestión del Proyecto

### Detener Airflow

```bash
make stop
```

### Ver logs en tiempo real

```bash
make logs
```

### Limpiar completamente (incluye volúmenes)

```bash
make clean
```

### Reconstruir después de cambios en Dockerfile

```bash
make build
make restart
```

## Notas Importantes

- Los logs se almacenan en la carpeta `logs/`
- Los DAGs se cargan desde la carpeta `dags/`
- Los plugins personalizados van en `plugins/`
- El archivo `.env` contiene credenciales sensibles y NO debe versionarse en Git
- La metadata de Airflow se almacena en PostgreSQL 14 (servidor empresa)

## Solución de Problemas

### Airflow no inicia

```bash
# Ver logs para identificar el error
make logs

# Verificar estado de contenedores
make status
```

### Problemas de conexión a PostgreSQL

Verifica que:
1. El servidor PostgreSQL esté accesible: `192.168.24.109:5433`
2. Las credenciales en `.env` sean correctas
3. El firewall permita la conexión al puerto 5433

### DAGs no aparecen en la UI

1. Verifica que el archivo esté en la carpeta `dags/`
2. Revisa que no tenga errores de sintaxis Python
3. Espera unos segundos (Airflow escanea cada 30 segundos)
4. Revisa los logs: `make logs-scheduler`

## Versiones

- Apache Airflow: 2.10.4
- Python: 3.11
- PostgreSQL: 14
- Executor: LocalExecutor

## Documentación Adicional

- [Documentación oficial de Airflow](https://airflow.apache.org/docs/)
- [Guía de DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Operadores disponibles](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)
