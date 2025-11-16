# Driver ODBC IBM i (AS/400) - Configuración

Este documento detalla la configuración del driver ODBC para IBM i (AS/400) DB2 en el proyecto Airflow.

## 📦 Driver Instalado

**Nombre:** IBM i Access ODBC Driver
**Versión:** 1.1.0.15-1.0
**Paquete:** `ibm-iaccess-1.1.0.15-1.0.amd64.deb`
**Ubicación:** `/home/paxo/airflow_develop/docker/ibm-iaccess-1.1.0.15-1.0.amd64.deb`

## 🏗️ Instalación en Docker

### Archivos Necesarios

```
docker/
├── Dockerfile                            # Configuración de instalación
├── ibm-iaccess-1.1.0.15-1.0.amd64.deb   # Driver IBM i Access (5.0 MB)
├── odbcinst.ini                          # Configuración de drivers ODBC
├── odbc.ini                              # Configuración de conexiones DSN
└── requirements.txt                      # Dependencias Python (pyodbc)
```

### Configuración en Dockerfile

```dockerfile
# Instalar unixODBC
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar driver IBM i Access ODBC
COPY docker/ibm-iaccess-1.1.0.15-1.0.amd64.deb /tmp/ibm-iaccess-1.1.0.15-1.0.amd64.deb
RUN dpkg -i /tmp/ibm-iaccess-1.1.0.15-1.0.amd64.deb || true && \
    apt-get update && \
    apt-get install -f -y && \
    ln -s /opt/ibm/iaccess/lib64/libcwb* /usr/lib/ && \
    rm /tmp/ibm-iaccess-1.1.0.15-1.0.amd64.deb

# Copiar configuración ODBC
COPY docker/odbcinst.ini /etc/odbcinst.ini
COPY docker/odbc.ini /etc/odbc.ini
```

## 📝 Archivos de Configuración

### odbcinst.ini

Ubicación: `/etc/odbcinst.ini`

```ini
[iSeries Access ODBC Driver]
Description=IBM i Access for Linux ODBC Driver
Driver64=/opt/ibm/iaccess/lib64/libcwbodbc.so
Setup64=/opt/ibm/iaccess/lib64/libcwbodbcs.so
Threading=0
DontDLClose=1
UsageCount=1
CPTimeout=120

[ODBC]
CPTimeout=120
```

**Campos importantes:**
- `Driver64` - Ubicación del driver ODBC de 64 bits
- `Setup64` - Ubicación de la librería de configuración
- `CPTimeout` - Timeout de conexión en segundos (120s = 2 minutos)

### odbc.ini

Ubicación: `/etc/odbc.ini`

```ini
[ODBC Data Sources]
DEV = DEV

[DEV]
Description = iSeries Access ODBC Driver
Driver = iSeries Access ODBC Driver
System = 192.168.24.1
UserID = WEBUSR
Password = idesa18
DefaultLibraries = QGPL
ExtendedDynamic = 1
DefaultPackage = A/DEFAULT(IBM),1,0,1,0,512
AllowDataCompression = 1
AllowUnsupportedChar = 1
ForceTranslation = 1
TrueAutoCommit = 1
DEBUG = 131072  ; FIXES PHP UTF-8 bug https://bugs.php.net/bug.php?id=47133
```

**Parámetros importantes:**

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `System` | 192.168.24.1 | IP del sistema IBM i |
| `UserID` | WEBUSR | Usuario de conexión |
| `Password` | idesa18 | Contraseña |
| `DefaultLibraries` | QGPL | Bibliotecas por defecto |
| `ExtendedDynamic` | 1 | Habilita SQL dinámico extendido |
| `AllowDataCompression` | 1 | Compresión de datos |
| `AllowUnsupportedChar` | 1 | Permite caracteres no soportados |
| `ForceTranslation` | 1 | Fuerza traducción de caracteres |
| `TrueAutoCommit` | 1 | Auto-commit verdadero |
| `DEBUG` | 131072 | Fix para bug UTF-8 en PHP |

## 🔧 Uso del Driver

### Opción 1: Usando DSN (Data Source Name)

```python
import pyodbc

# Conectar usando el DSN configurado en odbc.ini
conn = pyodbc.connect('DSN=DEV')
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

**Ventajas:**
- Configuración centralizada en `odbc.ini`
- No es necesario especificar credenciales en el código
- Más fácil de mantener

**Desventajas:**
- Las credenciales están en texto plano en `odbc.ini`
- No permite credenciales dinámicas

### Opción 2: Connection String Completo

```python
import pyodbc

# Connection string completo
connection_string = (
    "DRIVER={iSeries Access ODBC Driver};"
    "SYSTEM=192.168.24.1;"
    "UID=WEBUSR;"
    "PWD=idesa18;"
    "DefaultLibraries=QGPL;"
    "ExtendedDynamic=1;"
    "AllowDataCompression=1;"
    "AllowUnsupportedChar=1;"
    "ForceTranslation=1;"
    "TrueAutoCommit=1;"
)

conn = pyodbc.connect(connection_string, timeout=10)
cursor = conn.cursor()

# Usar la conexión
# ...

cursor.close()
conn.close()
```

**Ventajas:**
- Mayor control sobre parámetros de conexión
- Permite credenciales dinámicas
- No depende de archivos de configuración

**Desventajas:**
- Más verboso
- Credenciales en el código (usar variables de entorno)

### Opción 3: Usando Airflow Connection (Recomendado)

```python
from airflow.providers.odbc.hooks.odbc import OdbcHook

def consultar_ibmi():
    # Usa la conexión configurada en Airflow
    hook = OdbcHook(odbc_conn_id='ibmi_dev')
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM biblioteca.tabla")
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records
```

**Ventajas:**
- Credenciales gestionadas por Airflow
- Configuración mediante variables de entorno
- Más seguro (no expone credenciales en código)

## 📚 Bibliotecas y Tablas

### Formato de Nombres

IBM i DB2 usa bibliotecas (schemas) para organizar tablas:

```sql
-- Formato completo
SELECT * FROM biblioteca.tabla

-- Ejemplos
SELECT * FROM gxdbprueba.ubitfra
SELECT * FROM qgpl.qsqptabl
SELECT * FROM mylib.customers
```

### Nombres con Caracteres Especiales

Si la tabla o biblioteca tiene caracteres especiales o mayúsculas/minúsculas:

```sql
-- Usar comillas dobles
SELECT * FROM "MiLibreria"."MiTabla"
SELECT * FROM biblioteca."TABLA-CON-GUION"
```

### Biblioteca por Defecto

Puedes establecer una biblioteca por defecto en el connection string:

```python
"DefaultLibraries=BIBLIOTECA1,BIBLIOTECA2,QGPL;"
```

Esto permite consultar sin especificar la biblioteca:

```sql
-- Si DefaultLibraries=GXDBPRUEBA
SELECT * FROM ubitfra  -- Busca en GXDBPRUEBA.ubitfra
```

## 🔍 Consultas SQL

### Sintaxis Específica de DB2 for i

**FETCH FIRST (Limitar resultados):**
```sql
SELECT * FROM biblioteca.tabla
FETCH FIRST 10 ROWS ONLY
```

**FOR READ ONLY (Solo lectura):**
```sql
SELECT * FROM biblioteca.tabla
FOR READ ONLY
```

**WITH ISOLATION:**
```sql
SELECT * FROM biblioteca.tabla
WITH NONE  -- Sin bloqueo
```

### Metadatos del Sistema

**Listar tablas de una biblioteca:**
```sql
SELECT TABLE_NAME, TABLE_TYPE
FROM QSYS2.SYSTABLES
WHERE TABLE_SCHEMA = 'BIBLIOTECA'
ORDER BY TABLE_NAME
```

**Listar columnas de una tabla:**
```sql
SELECT COLUMN_NAME, DATA_TYPE, LENGTH
FROM QSYS2.SYSCOLUMNS
WHERE TABLE_SCHEMA = 'BIBLIOTECA'
  AND TABLE_NAME = 'TABLA'
ORDER BY ORDINAL_POSITION
```

**Información del sistema:**
```sql
SELECT OS_VERSION, OS_RELEASE
FROM SYSIBMADM.ENV_SYS_INFO
```

**Usuario actual:**
```sql
SELECT USER FROM SYSIBM.SYSDUMMY1
```

**Esquema actual:**
```sql
SELECT CURRENT SCHEMA FROM SYSIBM.SYSDUMMY1
```

## 🛠️ Troubleshooting

### Error: Driver not found

**Síntoma:**
```
pyodbc.Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'iSeries Access ODBC Driver'")
```

**Solución:**
1. Verificar que el driver esté instalado:
   ```bash
   docker exec -it airflow1-airflow-webserver-1 ls -l /opt/ibm/iaccess/lib64/
   ```

2. Verificar configuración en `/etc/odbcinst.ini`:
   ```bash
   docker exec -it airflow1-airflow-webserver-1 cat /etc/odbcinst.ini
   ```

3. Verificar symlinks:
   ```bash
   docker exec -it airflow1-airflow-webserver-1 ls -l /usr/lib/libcwb*
   ```

4. Si falta, reconstruir imagen:
   ```bash
   make build
   ```

### Error: Connection timeout

**Síntoma:**
```
pyodbc.Error: ('HYT00', '[HYT00] [unixODBC]Timeout expired')
```

**Soluciones:**
1. Verificar conectividad de red:
   ```bash
   docker exec -it airflow1-airflow-webserver-1 ping 192.168.24.1
   ```

2. Aumentar timeout en connection string:
   ```python
   conn = pyodbc.connect(connection_string, timeout=30)
   ```

3. Verificar VPN si es necesaria

4. Verificar firewall en el IBM i

### Error: Authentication failed

**Síntoma:**
```
pyodbc.Error: ('28000', '[28000] [IBM][System i Access ODBC Driver]Password expired')
```

**Soluciones:**
1. Verificar credenciales en `.env`:
   ```bash
   grep IBMI .env
   ```

2. Verificar usuario en IBM i no esté bloqueado o con password expirado

3. Probar credenciales desde otro cliente (JDBC, SSH, etc.)

### Error: Table not found

**Síntoma:**
```
pyodbc.ProgrammingError: ('42S02', '[42S02] [IBM][System i Access ODBC Driver][DB2 for i5/OS]SQL0204')
```

**Soluciones:**
1. Verificar nombre de biblioteca y tabla:
   ```sql
   SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_NAME LIKE '%NOMBRE%'
   ```

2. Usar mayúsculas si es necesario:
   ```sql
   SELECT * FROM GXDBPRUEBA.UBITFRA
   ```

3. Verificar permisos del usuario:
   ```sql
   -- Conectar como usuario con más privilegios
   -- Verificar privilegios sobre la tabla
   ```

### Error: UTF-8 encoding

**Síntoma:**
- Caracteres extraños en los datos
- Ñ, tildes o caracteres especiales incorrectos

**Soluciones:**
1. Agregar parámetro DEBUG en connection string:
   ```python
   "DEBUG=131072;"  # Fix UTF-8 bug
   ```

2. Usar `ForceTranslation=1` en connection string

3. Decodificar manualmente si es necesario:
   ```python
   value.decode('cp1252').encode('utf-8')
   ```

## 🔄 Actualizar Driver

Si necesitas actualizar a una versión más nueva del driver:

1. **Descargar nuevo driver:**
   - Obtener el nuevo `.deb` de IBM i Access
   - Copiarlo a `/home/paxo/airflow_develop/docker/`

2. **Actualizar Dockerfile:**
   ```dockerfile
   COPY docker/ibm-iaccess-X.X.X.X-X.X.amd64.deb /tmp/
   RUN dpkg -i /tmp/ibm-iaccess-X.X.X.X-X.X.amd64.deb ...
   ```

3. **Reconstruir imagen:**
   ```bash
   make build
   ```

4. **Reiniciar servicios:**
   ```bash
   make restart
   ```

5. **Verificar versión:**
   ```bash
   docker exec -it airflow1-airflow-webserver-1 dpkg -l | grep iaccess
   ```

## 📖 Referencias

- [IBM i Access Documentation](https://www.ibm.com/support/pages/ibm-i-access-client-solutions)
- [DB2 for i SQL Reference](https://www.ibm.com/docs/en/i/7.4?topic=reference-sql)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [unixODBC Documentation](http://www.unixodbc.org/)

## 📋 Checklist de Instalación

- [ ] Driver `.deb` copiado a `docker/`
- [ ] `odbcinst.ini` configurado
- [ ] `odbc.ini` configurado (opcional)
- [ ] Dockerfile actualizado con instalación
- [ ] `pyodbc` agregado a `requirements.txt`
- [ ] Imagen Docker reconstruida (`make build`)
- [ ] Servicios reiniciados (`make restart`)
- [ ] Conexión Airflow configurada en `.env`
- [ ] Variable de entorno en `docker-compose.yml`
- [ ] DAG de prueba creado
- [ ] Prueba exitosa de conexión

---

**Última actualización:** 2025-11-15
**Driver versión:** 1.1.0.15-1.0
**Sistema operativo:** Debian (base de Apache Airflow 3.1.3)
