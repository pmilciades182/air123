# DAGs de Airflow - Carpeta Local

Esta carpeta contiene los archivos de DAGs que se editan localmente y luego se despliegan a Airflow.

## 🔧 Configuración Rápida para VS Code

Si VS Code no reconoce las importaciones de Airflow (`Import "airflow..." could not be resolved`), ejecuta:

```bash
make setup-local
```

Este comando:
- ✅ Crea un entorno virtual Python local (`.venv`)
- ✅ Instala todas las dependencias de Airflow
- ✅ Configura VS Code automáticamente

Luego recarga VS Code y selecciona el intérprete `.venv/bin/python`.

**Nota:** El entorno `.venv` es SOLO para IntelliSense de VS Code. Airflow sigue ejecutándose en Docker.

## 📂 Estructura

```
dags_local/
├── README.md                 # Este archivo
├── ejemplo_dag.py           # DAG de ejemplo básico con tareas Python y Bash
├── dag_email_manual.py      # DAG para envío de emails (solo manual)
├── dag_postgres_test.py     # DAG para consultas PostgreSQL (solo manual)
└── dag_ibmi_test.py         # DAG para consultas IBM i DB2 (solo manual)
```

## 🚀 Flujo de Trabajo

### 1. Editar DAGs en esta carpeta

Crea o edita archivos `.py` en `dags_local/` usando tu editor favorito.

### 2. Desplegar a Airflow

```bash
# Desplegar un DAG específico
make deploy FILE=mi_dag.py

# Desplegar todos los DAGs
make deploy
```

### 3. Verificar en Airflow UI

Los DAGs aparecerán en la UI de Airflow en ~30 segundos después del deploy.

## 📋 DAGs Disponibles

### ejemplo_dag.py

**Descripción:** DAG de ejemplo básico que demuestra tareas Python y Bash.

- **Schedule:** Diario a las 8:00 AM
- **Tags:** ejemplo, tutorial
- **Tareas:**
  - Tarea de inicio
  - Verificación del sistema (Bash)
  - Procesamiento de datos
  - Finalización

### dag_email_manual.py

**Descripción:** Envía un correo electrónico de prueba usando SMTP.

- **Schedule:** Manual (solo se ejecuta al hacer trigger manual)
- **Tags:** email, manual
- **Conexión:** smtp_idesa
- **Tareas:**
  - Log de ejecución manual
  - Verificación de conectividad SMTP
  - Envío de email

**Destinatario:** pablo.gonzalez@idesa.com.py

### dag_postgres_test.py

**Descripción:** Consulta la tabla FRACCION en PostgreSQL.

- **Schedule:** Manual (solo se ejecuta al hacer trigger manual)
- **Tags:** postgres, test, manual
- **Conexión:** postgres_idesa
- **Tareas:**
  - Verificación de conexión PostgreSQL
  - Consulta a tabla FRACCION
  - Resumen de ejecución

**SQL:**
```sql
SELECT nfrac, centro_f, fecha, hora, usuario, estado
FROM public."FRACCION"
LIMIT 10;
```

### dag_ibmi_test.py

**Descripción:** Consulta la tabla ubitfra en IBM i DB2 (AS/400).

- **Schedule:** Manual (solo se ejecuta al hacer trigger manual)
- **Tags:** ibmi, db2, as400, test, manual
- **Conexión:** ibmi_dev
- **Tareas:**
  - Verificación de drivers ODBC
  - Verificación de conexión IBM i
  - Consulta a tabla ubitfra
  - Resumen de ejecución

**SQL:**
```sql
SELECT * FROM gxdbprueba.ubitfra
FETCH FIRST 10 ROWS ONLY
```

## ✏️ Crear un Nuevo DAG

### 1. Crear el archivo

```bash
# Copiar un ejemplo existente
cp dags_local/ejemplo_dag.py dags_local/mi_nuevo_dag.py

# O crear desde cero
nano dags_local/mi_nuevo_dag.py
```

### 2. Estructura básica de un DAG

```python
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Función de ejemplo
def mi_funcion():
    print("Hola desde Airflow!")

# Definición del DAG
with DAG(
    'mi_nuevo_dag',
    default_args=default_args,
    description='Descripción de mi DAG',
    schedule='0 8 * * *',  # Cron expression o None para manual
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['mi_tag'],
) as dag:

    tarea1 = PythonOperator(
        task_id='mi_tarea',
        python_callable=mi_funcion,
    )
```

### 3. Desplegar

```bash
make deploy FILE=mi_nuevo_dag.py
```

## 🔗 Usar Conexiones

Todas las conexiones están preconfiguradas mediante variables de entorno.

### SMTP

```python
from airflow.providers.smtp.operators.smtp import EmailOperator

enviar = EmailOperator(
    task_id='enviar_email',
    to='destinatario@example.com',
    subject='Asunto',
    html_content='<p>Contenido</p>',
    conn_id='smtp_idesa',
)
```

### PostgreSQL

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

def consultar():
    hook = PostgresHook(postgres_conn_id='postgres_idesa')
    records = hook.get_records("SELECT * FROM tabla")
    for record in records:
        print(record)
```

### IBM i DB2

```python
import pyodbc

def consultar():
    conn_string = (
        "DRIVER={iSeries Access ODBC Driver};"
        "SYSTEM=192.168.24.1;"
        "UID=WEBUSR;"
        "PWD=idesa18;"
    )
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM biblioteca.tabla")
    # ... procesar resultados
```

## 📅 Configurar Schedule

### Ejecución Manual (Sin Schedule)

```python
schedule=None
```

### Cron Expressions

```python
# Diario a las 8:00 AM
schedule='0 8 * * *'

# Cada hora
schedule='0 * * * *'

# Lunes a Viernes a las 9:00 AM
schedule='0 9 * * 1-5'

# Cada 15 minutos
schedule='*/15 * * * *'

# Primer día del mes a las 00:00
schedule='0 0 1 * *'
```

### Presets de Airflow

```python
from airflow.timetables.datasets import DatasetOrTimeSchedule

# Diario
schedule='@daily'

# Por hora
schedule='@hourly'

# Semanal
schedule='@weekly'

# Mensual
schedule='@monthly'
```

## 🏷️ Tags Recomendados

Usa tags para organizar tus DAGs:

```python
tags=['produccion', 'etl', 'diario']
tags=['desarrollo', 'test', 'manual']
tags=['reportes', 'mensual']
tags=['integracion', 'api', 'tiempo_real']
```

## 📖 Documentación Completa

Para más información sobre conexiones, configuración y troubleshooting, consulta:

- **[CONEXIONES_Y_DAGS.md](../CONEXIONES_Y_DAGS.md)** - Documentación completa de conexiones
- **[README.md](../README.md)** - Documentación general del proyecto
- **[README_SETUP.md](../README_SETUP.md)** - Guía de configuración

## 🔍 Tips y Buenas Prácticas

### 1. Nombres de DAGs

- Usa nombres descriptivos y únicos
- Usa snake_case: `mi_dag_ejemplo`
- Evita espacios y caracteres especiales

### 2. Nombres de Tareas

- Usa verbos de acción: `extraer_datos`, `transformar`, `cargar`
- Sé descriptivo pero conciso
- Usa snake_case

### 3. Manejo de Errores

```python
from airflow.exceptions import AirflowException

def mi_funcion():
    try:
        # Tu código
        pass
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise AirflowException(error_msg)
```

### 4. Logging

```python
def mi_funcion():
    print("=" * 60)
    print("INICIANDO PROCESO")
    print("=" * 60)
    print(f"Fecha: {datetime.now()}")
    # Tu código
    print("Proceso completado exitosamente")
```

### 5. XCom para Compartir Datos

```python
def tarea1(**context):
    resultado = "mi_valor"
    context['ti'].xcom_push(key='mi_key', value=resultado)

def tarea2(**context):
    valor = context['ti'].xcom_pull(key='mi_key', task_ids='tarea1')
    print(f"Valor recibido: {valor}")
```

### 6. DAGs Solo Manual

Para DAGs que solo deben ejecutarse manualmente:

```python
with DAG(
    'mi_dag_manual',
    schedule=None,  # IMPORTANTE: Sin schedule
    tags=['manual'],  # Tag para identificar
    # ... resto de configuración
) as dag:
    # ...
```

## ⚠️ Notas Importantes

- Los archivos en `dags_local/` son editables con permisos de tu usuario
- La carpeta `dags/` (donde se despliegan) tiene permisos del contenedor Docker
- Siempre edita en `dags_local/`, nunca directamente en `dags/`
- Los cambios en `dags_local/` NO se reflejan automáticamente, debes hacer `make deploy`
- Los DAGs se versionan en Git (están en el repositorio)
- NO incluyas credenciales hardcodeadas, usa conexiones de Airflow

---

**Última actualización:** 2025-11-15
