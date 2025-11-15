# Conexiones y DAGs de Ejemplo

Este documento describe todas las conexiones configuradas en Airflow y los DAGs de ejemplo disponibles.

## Índice

- [Conexiones Configuradas](#conexiones-configuradas)
  - [SMTP - Envío de Correos](#smtp---envío-de-correos)
  - [PostgreSQL - Base de Datos Planos](#postgresql---base-de-datos-planos)
  - [IBM i DB2 - AS/400](#ibm-i-db2---as400)
- [DAGs de Ejemplo](#dags-de-ejemplo)
- [Agregar Nuevas Conexiones](#agregar-nuevas-conexiones)

---

## Conexiones Configuradas

Todas las conexiones están preconfiguradas mediante variables de entorno en el archivo `.env`, lo que significa que están disponibles automáticamente sin necesidad de configurarlas manualmente en la UI de Airflow.

### SMTP - Envío de Correos

**ID de Conexión:** `smtp_idesa`

**Configuración:**
- **Servidor:** 192.168.250.30
- **Puerto:** 25
- **Autenticación:** No requiere
- **Email saliente:** airflow@idesa.com.py

**Variable de entorno (.env):**
```bash
AIRFLOW_CONN_SMTP_IDESA=smtp://:@192.168.250.30:25/?from_email=airflow@idesa.com.py
```

**Uso en DAGs:**
```python
from airflow.providers.smtp.operators.smtp import EmailOperator

enviar_email = EmailOperator(
    task_id='enviar_email',
    to='destinatario@idesa.com.py',
    subject='Asunto del correo',
    html_content='<p>Contenido del correo</p>',
    conn_id='smtp_idesa',
)
```

**DAG de Ejemplo:** `dag_email_manual.py`

---

### PostgreSQL - Base de Datos Planos

**ID de Conexión:** `postgres_idesa`

**Configuración:**
- **Host:** 192.168.24.109
- **Puerto:** 5433
- **Base de datos:** planos
- **Usuario:** postgres
- **Password:** 5PASzT0@iB

**Variable de entorno (.env):**
```bash
# Nota: El carácter @ en la password debe ser URL-encoded como %40
AIRFLOW_CONN_POSTGRES_IDESA=postgresql://postgres:5PASzT0%40iB@192.168.24.109:5433/planos
```

**Uso en DAGs:**

**Opción 1: Usando PostgresHook**
```python
from airflow.providers.postgres.hooks.postgres import PostgresHook

def consultar_postgres():
    pg_hook = PostgresHook(postgres_conn_id='postgres_idesa')

    # Obtener registros
    sql = "SELECT * FROM public.mi_tabla LIMIT 10"
    records = pg_hook.get_records(sql)

    # Imprimir resultados
    for record in records:
        print(record)
```

**Opción 2: Usando PostgresOperator**
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

consulta = PostgresOperator(
    task_id='ejecutar_consulta',
    postgres_conn_id='postgres_idesa',
    sql='SELECT * FROM public.mi_tabla',
)
```

**DAG de Ejemplo:** `dag_postgres_test.py`

---

### IBM i DB2 - AS/400

**ID de Conexión:** `ibmi_dev`

**Configuración:**
- **Sistema:** 192.168.24.1
- **Usuario:** WEBUSR
- **Password:** idesa18
- **Driver:** iSeries Access ODBC Driver
- **Biblioteca por defecto:** QGPL

**Variable de entorno (.env):**
```bash
AIRFLOW_CONN_IBMI_DEV=odbc://WEBUSR:idesa18@192.168.24.1/?driver=iSeries+Access+ODBC+Driver&DefaultLibraries=QGPL&ExtendedDynamic=1&AllowDataCompression=1&AllowUnsupportedChar=1&ForceTranslation=1&TrueAutoCommit=1
```

**Driver ODBC Instalado:**
- Paquete: `ibm-iaccess-1.1.0.15-1.0.amd64.deb`
- Ubicación driver: `/opt/ibm/iaccess/lib64/libcwbodbc.so`
- Configuración: `/etc/odbcinst.ini` y `/etc/odbc.ini`

**Uso en DAGs:**
```python
import pyodbc

def consultar_ibmi():
    connection_string = (
        f"DRIVER={{iSeries Access ODBC Driver}};"
        f"SYSTEM=192.168.24.1;"
        f"UID=WEBUSR;"
        f"PWD=idesa18;"
        f"DefaultLibraries=QGPL;"
    )

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Ejecutar consulta
    cursor.execute("SELECT * FROM biblioteca.tabla")
    records = cursor.fetchall()

    # Procesar resultados
    for record in records:
        print(record)

    cursor.close()
    conn.close()
```

**DAG de Ejemplo:** `dag_ibmi_test.py`

**Notas importantes:**
- El driver ODBC está instalado en el contenedor Docker
- La configuración ODBC permite usar tanto el nombre del driver como DSN
- Para consultas a tablas, usar el formato: `biblioteca.tabla`
- El driver soporta UTF-8 mediante el parámetro DEBUG=131072

---

## DAGs de Ejemplo

Todos los DAGs de ejemplo están configurados con `schedule=None`, lo que significa que **solo se ejecutan manualmente**.

### 1. dag_email_manual.py

**Descripción:** Envía un correo electrónico de prueba usando SMTP.

**Tareas:**
1. `log_ejecucion_manual` - Registra que el DAG fue ejecutado manualmente
2. `verificar_conectividad_smtp` - Verifica conectividad con el servidor SMTP
3. `enviar_email` - Envía el email de prueba

**Destinatario:** pablo.gonzalez@idesa.com.py
**Asunto:** test
**Cuerpo:** test

**Cómo ejecutar:**
1. Ir a la UI de Airflow (http://localhost:4000)
2. Buscar `dag_email_manual`
3. Hacer clic en el botón "Play" (▶)

**Logs esperados:**
- Verificación de conectividad TCP al servidor SMTP
- Verificación del protocolo SMTP
- Confirmación de envío del email

---

### 2. dag_postgres_test.py

**Descripción:** Consulta la tabla FRACCION en la base de datos PostgreSQL.

**Tareas:**
1. `verificar_conexion_postgres` - Verifica conexión y muestra info del servidor
2. `consultar_tabla_fraccion` - Ejecuta SELECT en la tabla FRACCION
3. `resumen_ejecucion` - Muestra resumen de la ejecución

**Consulta SQL:**
```sql
SELECT nfrac, centro_f, fecha, hora, usuario, estado
FROM public."FRACCION"
LIMIT 10;
```

**Cómo ejecutar:**
1. Ir a la UI de Airflow (http://localhost:4000)
2. Buscar `dag_postgres_test`
3. Hacer clic en el botón "Play" (▶)

**Logs esperados:**
- Versión de PostgreSQL
- Base de datos y usuario actual
- Tabla con los primeros 10 registros de FRACCION
- Formato: nfrac | centro_f | fecha | hora | usuario | estado

---

### 3. dag_ibmi_test.py

**Descripción:** Consulta la tabla ubitfra en IBM i DB2 (AS/400).

**Tareas:**
1. `verificar_driver_odbc` - Lista drivers ODBC disponibles
2. `verificar_conexion_ibmi` - Verifica conexión al sistema IBM i
3. `consultar_tabla_ubitfra` - Ejecuta SELECT en la tabla
4. `resumen_ejecucion` - Muestra resumen de la ejecución

**Consulta SQL:**
```sql
SELECT * FROM gxdbprueba.ubitfra
FETCH FIRST 10 ROWS ONLY
```

**Cómo ejecutar:**
1. Ir a la UI de Airflow (http://localhost:4000)
2. Buscar `dag_ibmi_test`
3. Hacer clic en el botón "Play" (▶)

**Logs esperados:**
- Lista de drivers ODBC instalados
- Confirmación del driver "iSeries Access ODBC Driver"
- Versión del OS IBM i
- Tabla con los primeros 10 registros de ubitfra

**Solución de problemas:**
- Si el driver no aparece, verificar que la imagen Docker se haya reconstruido con `make build`
- Si hay error de conexión, verificar conectividad de red al sistema 192.168.24.1
- Si hay error de permisos, verificar que el usuario WEBUSR tenga acceso a la tabla

---

## Agregar Nuevas Conexiones

### Paso 1: Agregar al archivo .env

Edita el archivo `.env` y agrega la nueva conexión. El formato varía según el tipo:

**PostgreSQL:**
```bash
AIRFLOW_CONN_MI_POSTGRES=postgresql://usuario:password@host:puerto/database
```

**MySQL:**
```bash
AIRFLOW_CONN_MI_MYSQL=mysql://usuario:password@host:puerto/database
```

**SQL Server:**
```bash
AIRFLOW_CONN_MI_SQLSERVER=mssql+pyodbc://usuario:password@host:puerto/database?driver=ODBC+Driver+17+for+SQL+Server
```

**HTTP/API:**
```bash
AIRFLOW_CONN_MI_API=http://usuario:password@host:puerto
```

**SFTP:**
```bash
AIRFLOW_CONN_MI_SFTP=sftp://usuario:password@host:puerto
```

**Notas importantes:**
- El ID de conexión se toma del sufijo después de `AIRFLOW_CONN_`
  - Ejemplo: `AIRFLOW_CONN_MI_DB` → ID = `mi_db`
- Los caracteres especiales en passwords deben ser URL-encoded:
  - `@` → `%40`
  - `#` → `%23`
  - `%` → `%25`
  - `:` → `%3A`
  - `/` → `%2F`
- Los espacios en nombres deben ser `+` o `%20`

### Paso 2: Agregar al docker-compose.yml

Edita `docker-compose.yml` y agrega la variable de entorno en la sección `environment`:

```yaml
environment:
  &airflow-common-env
  AIRFLOW__CORE__EXECUTOR: LocalExecutor
  # ... otras variables ...
  AIRFLOW_CONN_MI_NUEVA_CONEXION: ${AIRFLOW_CONN_MI_NUEVA_CONEXION}
```

### Paso 3: Documentar en archivos .env.example

Actualiza los siguientes archivos para documentar la nueva conexión:
- `.env.example`
- `.env.example.local`
- `.env.instance2.example`

Agrega una sección como esta:

```bash
# ==============================================================================
# CONEXIÓN MI SISTEMA
# ==============================================================================
# Descripción de la conexión
# Formato: tipo://usuario:password@host:puerto/database
AIRFLOW_CONN_MI_CONEXION=postgresql://user:pass@host:5432/db
```

### Paso 4: Instalar dependencias si es necesario

Si la conexión requiere un provider específico de Airflow, agrégalo a `docker/requirements.txt`:

```bash
# Para MySQL
apache-airflow-providers-mysql>=5.0.0

# Para SQL Server
apache-airflow-providers-microsoft-mssql>=4.0.0

# Para Oracle
apache-airflow-providers-oracle>=4.0.0

# Para MongoDB
apache-airflow-providers-mongo>=4.0.0

# Para AWS
apache-airflow-providers-amazon>=8.0.0
```

### Paso 5: Reconstruir y reiniciar

```bash
# Si agregaste dependencias nuevas en requirements.txt
make build

# Reiniciar para cargar las nuevas variables de entorno
make restart
```

### Paso 6: Crear un DAG de prueba

Crea un DAG de ejemplo en `dags_local/` para probar la conexión:

```python
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

def probar_conexion():
    # Tu código para probar la conexión
    print("Conexión exitosa!")

with DAG(
    'dag_test_mi_conexion',
    schedule=None,  # Solo manual
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['test', 'manual'],
) as dag:

    test = PythonOperator(
        task_id='probar_conexion',
        python_callable=probar_conexion,
    )
```

Despliega y prueba:

```bash
make deploy FILE=dag_test_mi_conexion.py
```

---

## Drivers ODBC Instalados

Los siguientes drivers ODBC están instalados en el contenedor:

### 1. iSeries Access ODBC Driver (IBM i / AS/400)
- **Versión:** 1.1.0.15
- **Archivo:** `/opt/ibm/iaccess/lib64/libcwbodbc.so`
- **Configuración:** `/etc/odbcinst.ini`, `/etc/odbc.ini`
- **DSN configurado:** DEV (apunta a 192.168.24.1)

### 2. ODBC Driver 17 for SQL Server
- **Archivo:** `/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.6.1`
- **Uso:** Para conectar a bases de datos Microsoft SQL Server

### Verificar drivers disponibles

Puedes verificar los drivers ODBC disponibles ejecutando el DAG `dag_ibmi_test.py` y revisando los logs de la tarea `verificar_driver_odbc`, o ejecutando este comando en el contenedor:

```python
import pyodbc
drivers = pyodbc.drivers()
for driver in drivers:
    print(driver)
```

---

## Consideraciones de Seguridad

### Passwords en Variables de Entorno

Las passwords están almacenadas en el archivo `.env` que **NO debe versionarse en Git**. El archivo `.gitignore` ya está configurado para excluir `.env`.

### Rotación de Credenciales

Si necesitas cambiar las credenciales:

1. Actualiza el archivo `.env`
2. Reinicia Airflow: `make restart`
3. No es necesario reconstruir la imagen

### Múltiples Instancias

Si tienes múltiples instancias de Airflow en el mismo servidor:
- Cada instancia tiene su propio archivo `.env`
- Las conexiones pueden ser diferentes en cada instancia
- Las credenciales no se comparten entre instancias

---

## Solución de Problemas Comunes

### Error: Connection not found

**Causa:** La variable de entorno no está cargada correctamente.

**Solución:**
1. Verificar que la variable esté en `.env`
2. Verificar que esté en `docker-compose.yml`
3. Reiniciar Airflow: `make restart`

### Error: Driver not found (ODBC)

**Causa:** El driver ODBC no está instalado en el contenedor.

**Solución:**
1. Verificar que el Dockerfile instale el driver
2. Reconstruir la imagen: `make build`
3. Reiniciar: `make restart`

### Error: Timeout al conectar

**Causa:** El servidor no es accesible desde el contenedor.

**Solución:**
1. Verificar conectividad de red (firewall, VPN)
2. Verificar que el host/IP sea correcto
3. Verificar que el puerto esté abierto
4. Revisar logs del DAG para más detalles

### Error: Authentication failed

**Causa:** Credenciales incorrectas.

**Solución:**
1. Verificar usuario y password en `.env`
2. Verificar caracteres especiales estén URL-encoded
3. Probar las credenciales manualmente desde otro cliente

---

## Recursos Adicionales

- [Documentación de Airflow Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html)
- [Airflow Providers](https://airflow.apache.org/docs/apache-airflow-providers/)
- [Connection Types](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/connection.html)
- [IBM i Access ODBC Driver Documentation](https://www.ibm.com/support/pages/ibm-i-access-client-solutions)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)

---

**Última actualización:** 2025-11-15
**Versión de Airflow:** 3.1.3
**Python:** 3.13
