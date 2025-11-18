# 📚 Airflow IDESA - Documentación

> **Proyecto de orquestación de tareas con Apache Airflow 3.1.3**

## 🗂️ Estructura de Documentación

```
airflow_develop/
│
├── 📄 README.md                          # Documentación principal del proyecto
├── 📄 DOCUMENTATION.md                   # Este archivo - Índice de documentación
│
├── 📁 docs/                              # Documentación técnica completa
│   ├── 📄 README.md                      # Índice principal de documentación
│   ├── 🚀 installation-guide.md          # Guía de instalación y configuración
│   ├── 🔌 connections-configuration.md   # Configuración de conexiones
│   ├── 📝 dag-development-guide.md       # Guía de desarrollo de DAGs
│   └── 🔧 ibmi-odbc-driver-setup.md     # Setup del driver ODBC IBM i
│
├── 📁 dags_local/                        # DAGs editables localmente
│   ├── 📄 README.md                      # Guía rápida de desarrollo de DAGs
│   ├── ejemplo_dag.py                    # DAG de ejemplo básico
│   ├── dag_email_manual.py              # DAG de prueba SMTP
│   ├── dag_postgres_test.py             # DAG de prueba PostgreSQL
│   └── dag_ibmi_test.py                 # DAG de prueba IBM i DB2
│
├── 📁 docker/                            # Configuración Docker
│   ├── Dockerfile                        # Imagen customizada de Airflow
│   ├── requirements.txt                  # Dependencias Python
│   ├── ibm-iaccess-*.deb                # Driver ODBC IBM i
│   ├── odbcinst.ini                     # Config drivers ODBC
│   └── odbc.ini                         # Config conexiones ODBC
│
└── 📁 logs/                              # Logs de Airflow (generado)
```

---

## 🎯 Inicio Rápido

### Para Nuevos Usuarios

1. **Lee primero:** [README.md](README.md) - Overview del proyecto
2. **Instala:** [docs/installation-guide.md](docs/installation-guide.md)
3. **Explora:** [docs/README.md](docs/README.md) - Índice completo

### Para Desarrolladores

1. **Desarrollo de DAGs:** [dags_local/README.md](dags_local/README.md)
2. **Usar conexiones:** [docs/connections-configuration.md](docs/connections-configuration.md)
3. **Ejemplos:** Revisa los DAGs en `dags_local/`

### Para Administradores

1. **Instalación:** [docs/installation-guide.md](docs/installation-guide.md)
2. **Configurar conexiones:** [docs/connections-configuration.md](docs/connections-configuration.md)
3. **Setup ODBC:** [docs/ibmi-odbc-driver-setup.md](docs/ibmi-odbc-driver-setup.md)

---

## 📖 Guías Principales

### 🚀 [Installation Guide](docs/installation-guide.md)

**Contenido:**
- Configuración inicial del proyecto
- Variables de entorno
- Generación de claves de seguridad
- Setup de base de datos PostgreSQL
- Configuración de múltiples instancias
- Comandos útiles del Makefile
- Troubleshooting de instalación

**Cuándo leer:**
- Primera instalación
- Configurar nueva instancia
- Problemas de instalación

---

### 🔌 [Connections Configuration](docs/connections-configuration.md)

**Contenido:**
- Conexiones disponibles (SMTP, PostgreSQL, IBM i DB2)
- Configuración mediante variables de entorno
- Ejemplos de uso en DAGs
- Agregar nuevas conexiones
- Solución de problemas de conectividad
- Consideraciones de seguridad

**Cuándo leer:**
- Usar conexiones existentes en DAGs
- Agregar nuevas conexiones
- Troubleshooting de conexiones

---

### 📝 [DAG Development Guide](docs/dag-development-guide.md)

**Contenido:**
- Flujo de trabajo para crear DAGs
- Estructura de `dags_local/`
- Plantillas y ejemplos
- Uso de conexiones en DAGs
- Configuración de schedules
- Tips y mejores prácticas
- Convenciones de nomenclatura

**Cuándo leer:**
- Crear nuevos DAGs
- Aprender mejores prácticas
- Ejemplos de código

**También disponible en:** [dags_local/README.md](dags_local/README.md)

---

### 🔧 [IBM i ODBC Driver Setup](docs/ibmi-odbc-driver-setup.md)

**Contenido:**
- Instalación del driver IBM i Access ODBC
- Configuración en Docker
- Archivos de configuración ODBC
- Uso del driver con pyodbc
- Sintaxis SQL específica de DB2 for i
- Troubleshooting detallado del driver
- Actualización del driver

**Cuándo leer:**
- Trabajar con IBM i (AS/400)
- Problemas con el driver ODBC
- Actualizar el driver

---

## 🔍 Buscar por Tema

### Conexiones

| Sistema | Guía Principal | Detalles Técnicos |
|---------|---------------|-------------------|
| **SMTP** | [Connections Configuration](docs/connections-configuration.md#smtp---envío-de-correos) | Variables de entorno |
| **PostgreSQL** | [Connections Configuration](docs/connections-configuration.md#postgresql---base-de-datos-planos) | PostgresHook, SQL |
| **IBM i DB2** | [IBM i ODBC Driver Setup](docs/ibmi-odbc-driver-setup.md) | Driver ODBC, pyodbc |

### Desarrollo

| Tarea | Documentación |
|-------|---------------|
| Crear un DAG | [DAG Development Guide](docs/dag-development-guide.md#crear-un-nuevo-dag) |
| Usar PostgreSQL | [DAG Development Guide](docs/dag-development-guide.md#postgresql) |
| Usar IBM i | [DAG Development Guide](docs/dag-development-guide.md#ibm-i-db2) |
| Enviar emails | [DAG Development Guide](docs/dag-development-guide.md#smtp) |
| Schedules | [DAG Development Guide](docs/dag-development-guide.md#configurar-schedule) |

### Operaciones

| Operación | Documentación |
|-----------|---------------|
| Instalar | [Installation Guide](docs/installation-guide.md#inicio-rápido---primera-instancia) |
| Segunda instancia | [Installation Guide](docs/installation-guide.md#múltiples-instancias-en-el-mismo-servidor) |
| Desplegar DAGs | [README](README.md#flujo-de-trabajo-para-dags) |
| Troubleshooting | Ver sección específica en cada guía |

---

## 🛠️ Comandos Rápidos

```bash
# Ver toda la ayuda disponible
make help

# Construir imagen Docker
make build

# Iniciar Airflow
make start

# Desplegar DAGs
make deploy
make deploy FILE=mi_dag.py

# Ver logs
make logs

# Reiniciar servicios
make restart
```

**Más comandos:** [Installation Guide - Comandos Disponibles](docs/installation-guide.md#comandos-disponibles-makefile)

---

## 🔐 Información Importante

### Archivos Sensibles (NO versionar)

- ❌ `.env` - Credenciales y configuración
- ❌ `logs/` - Logs de ejecución
- ❌ `dags/` - DAGs desplegados (generado)

### Archivos Versionados

- ✅ `dags_local/` - DAGs fuente
- ✅ `docs/` - Documentación
- ✅ `docker/` - Configuración Docker
- ✅ `.env.example*` - Plantillas de configuración

---

## 📊 Tecnologías

| Componente | Versión | Documentación |
|------------|---------|---------------|
| Apache Airflow | 3.1.3 | [Oficial](https://airflow.apache.org/docs/apache-airflow/3.1.3/) |
| Python | 3.13 | [Oficial](https://docs.python.org/3.13/) |
| PostgreSQL | 14 | [Oficial](https://www.postgresql.org/docs/14/) |
| Docker | Latest | [Oficial](https://docs.docker.com/) |
| IBM i Access ODBC | 1.1.0.15 | [Docs](docs/ibmi-odbc-driver-setup.md) |

---

## 🎓 Recursos de Aprendizaje

### Documentación Oficial Airflow

- [Conceptos: DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Conceptos: Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)
- [Conceptos: Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html)
- [API Reference](https://airflow.apache.org/docs/apache-airflow/stable/python-api-ref.html)

### Providers

- [PostgreSQL Provider](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/)
- [SMTP Provider](https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/)
- [ODBC Provider](https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/)

---

## 💡 Tips Rápidos

### Para Desarrolladores

```python
# DAG solo manual (no programado)
with DAG('mi_dag', schedule=None, ...):

# Usar conexión PostgreSQL
from airflow.providers.postgres.hooks.postgres import PostgresHook
hook = PostgresHook(postgres_conn_id='postgres_idesa')

# Usar conexión IBM i
import pyodbc
conn = pyodbc.connect("DSN=DEV")
```

### Para Administradores

```bash
# Cambiar credenciales de una conexión
# 1. Editar .env
nano .env

# 2. Reiniciar (NO es necesario rebuild)
make restart

# Agregar nueva conexión
# 1. Agregar a .env
# 2. Agregar a docker-compose.yml (environment)
# 3. Reiniciar
```

---

## 📞 Soporte y Contribución

### Problemas Comunes

1. **DAG no aparece:** Ver [Troubleshooting](docs/installation-guide.md#problema-dags-no-aparecen-en-la-ui)
2. **Error de conexión:** Ver [Connections Troubleshooting](docs/connections-configuration.md#solución-de-problemas-comunes)
3. **Driver ODBC:** Ver [IBM i Troubleshooting](docs/ibmi-odbc-driver-setup.md#troubleshooting)

### Flujo de Trabajo

```
1. Leer documentación → 2. Editar en dags_local/ → 3. make deploy → 4. Probar en UI
```

---

## 📅 Última Actualización

**Versión:** 1.0.0
**Fecha:** 2025-11-15
**Mantenido por:** Equipo de Desarrollo IDESA

---

## 🗺️ Mapa del Sitio de Documentación

```
docs/
├── README.md                          ← Empezar aquí (índice completo)
│
├── installation-guide.md              ← Setup inicial
│   ├── Primera instalación
│   ├── Múltiples instancias
│   ├── Configuración
│   └── Troubleshooting
│
├── connections-configuration.md       ← Conexiones
│   ├── SMTP
│   ├── PostgreSQL
│   ├── IBM i DB2
│   ├── Agregar nuevas
│   └── Troubleshooting
│
├── dag-development-guide.md          ← Desarrollo
│   ├── Crear DAGs
│   ├── Ejemplos
│   ├── Schedules
│   └── Mejores prácticas
│
└── ibmi-odbc-driver-setup.md        ← IBM i específico
    ├── Instalación driver
    ├── Configuración
    ├── Uso
    └── Troubleshooting
```

---

**[⬆ Volver al inicio](#-airflow-idesa---documentación)**
