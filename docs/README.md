# Airflow IDESA - Documentación Técnica

Documentación completa del proyecto Apache Airflow para orquestación de tareas.

## 📋 Índice de Documentación

### 🚀 Inicio Rápido

1. **[Installation Guide](installation-guide.md)**
   - Configuración inicial del proyecto
   - Configuración de variables de entorno
   - Generación de claves de seguridad
   - Creación de base de datos PostgreSQL
   - Configuración de múltiples instancias
   - Verificación de la instalación

### 🔌 Configuración de Conexiones

2. **[Connections Configuration](connections-configuration.md)**
   - Conexiones disponibles (SMTP, PostgreSQL, IBM i DB2)
   - Configuración mediante variables de entorno
   - Uso de conexiones en DAGs
   - Agregar nuevas conexiones
   - Solución de problemas
   - Consideraciones de seguridad

### 📝 Desarrollo de DAGs

3. **[DAG Development Guide](dag-development-guide.md)**
   - Estructura de la carpeta `dags_local/`
   - Flujo de trabajo para crear DAGs
   - DAGs de ejemplo disponibles
   - Plantillas y ejemplos de código
   - Uso de conexiones en DAGs
   - Configuración de schedules
   - Tips y mejores prácticas

### 🔧 Drivers y Extensiones

4. **[IBM i ODBC Driver Setup](ibmi-odbc-driver-setup.md)**
   - Instalación del driver IBM i Access ODBC
   - Configuración en Docker
   - Archivos de configuración (odbcinst.ini, odbc.ini)
   - Uso del driver en Python (pyodbc)
   - Sintaxis SQL específica de DB2 for i
   - Troubleshooting detallado
   - Actualización del driver

## 🗂️ Estructura de la Documentación

```
docs/
├── README.md                        # Este archivo - Índice principal
├── installation-guide.md            # Guía de instalación y setup
├── connections-configuration.md     # Configuración de conexiones
├── dag-development-guide.md         # Desarrollo de DAGs
├── ibmi-odbc-driver-setup.md       # Setup driver ODBC IBM i
└── architecture-overview.md         # Arquitectura del proyecto (próximamente)
```

## 🎯 Guías por Caso de Uso

### Para Administradores

**Configurar una nueva instancia de Airflow:**
1. [Installation Guide](installation-guide.md) → Sección "Inicio Rápido - Primera Instancia"
2. [Connections Configuration](connections-configuration.md) → Verificar conexiones disponibles

**Agregar una segunda instancia:**
1. [Installation Guide](installation-guide.md) → Sección "Múltiples Instancias"

**Configurar nuevas conexiones:**
1. [Connections Configuration](connections-configuration.md) → Sección "Agregar Nuevas Conexiones"

### Para Desarrolladores

**Crear un nuevo DAG:**
1. [DAG Development Guide](dag-development-guide.md) → Sección "Crear un Nuevo DAG"
2. [DAG Development Guide](dag-development-guide.md) → Sección "Usar Conexiones"

**Conectar a PostgreSQL:**
1. [Connections Configuration](connections-configuration.md) → Sección "PostgreSQL"
2. [DAG Development Guide](dag-development-guide.md) → Ejemplos de código PostgreSQL

**Conectar a IBM i (AS/400):**
1. [IBM i ODBC Driver Setup](ibmi-odbc-driver-setup.md) → Sección "Uso del Driver"
2. [DAG Development Guide](dag-development-guide.md) → Ejemplos de código IBM i

**Enviar emails desde DAGs:**
1. [Connections Configuration](connections-configuration.md) → Sección "SMTP"
2. [DAG Development Guide](dag-development-guide.md) → Ejemplos de código SMTP

### Para Troubleshooting

**Problemas con conexiones:**
1. [Connections Configuration](connections-configuration.md) → Sección "Solución de Problemas Comunes"

**Problemas con driver ODBC IBM i:**
1. [IBM i ODBC Driver Setup](ibmi-odbc-driver-setup.md) → Sección "Troubleshooting"

**Problemas de instalación:**
1. [Installation Guide](installation-guide.md) → Sección "Solución de Problemas"

## 📚 Recursos Externos

### Documentación Oficial de Apache Airflow

- [Airflow 3.1.3 Documentation](https://airflow.apache.org/docs/apache-airflow/3.1.3/)
- [Concepts: DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Concepts: Operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)
- [Concepts: Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html)
- [Airflow 3.0 Migration Guide](https://airflow.apache.org/docs/apache-airflow/3.1.3/migrations-ref.html)

### Airflow Providers

- [All Providers](https://airflow.apache.org/docs/apache-airflow-providers/)
- [PostgreSQL Provider](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/)
- [SMTP Provider](https://airflow.apache.org/docs/apache-airflow-providers-smtp/stable/)
- [ODBC Provider](https://airflow.apache.org/docs/apache-airflow-providers-odbc/stable/)

### Tecnologías Relacionadas

- [PostgreSQL 14 Documentation](https://www.postgresql.org/docs/14/)
- [IBM i Access Documentation](https://www.ibm.com/support/pages/ibm-i-access-client-solutions)
- [DB2 for i SQL Reference](https://www.ibm.com/docs/en/i/7.4?topic=reference-sql)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [Docker Documentation](https://docs.docker.com/)

## 🔄 Versionamiento

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-11-15 | Versión inicial con conexiones SMTP, PostgreSQL e IBM i DB2 |

## 📞 Soporte

Para problemas o preguntas:

1. Revisar la sección de troubleshooting en cada guía
2. Consultar la documentación oficial de Airflow
3. Contactar al equipo de desarrollo

## 🔐 Seguridad

**Importante:**
- Nunca versionar el archivo `.env` (ya está en `.gitignore`)
- Las credenciales deben estar solo en variables de entorno
- Usar conexiones de Airflow en lugar de hardcodear credenciales
- Rotar credenciales periódicamente

Ver [Connections Configuration](connections-configuration.md) → Sección "Consideraciones de Seguridad" para más detalles.

## 🏗️ Arquitectura

### Componentes Principales

- **Airflow Webserver** - Interfaz web y API server
- **Airflow Scheduler** - Programador de tareas
- **Airflow Triggerer** - Gestor de tareas asíncronas
- **Airflow DAG Processor** - Procesador de archivos de DAGs
- **PostgreSQL 14** - Base de datos de metadata

### Tecnologías

- **Apache Airflow:** 3.1.3
- **Python:** 3.13
- **PostgreSQL:** 14
- **Executor:** LocalExecutor
- **Containerización:** Docker / Docker Compose

## 📝 Convenciones

### Nomenclatura de DAGs

- Usar `snake_case` para nombres de DAGs
- Prefijos recomendados:
  - `etl_` - Procesos ETL
  - `report_` - Generación de reportes
  - `sync_` - Sincronizaciones
  - `backup_` - Respaldos
  - `test_` - DAGs de prueba
  - `dag_` - DAGs genéricos

### Nomenclatura de Tareas

- Usar `snake_case` para task_ids
- Usar verbos de acción: `extract_`, `transform_`, `load_`, `validate_`
- Ser descriptivo pero conciso

### Tags

- Usar tags para categorizar DAGs
- Tags comunes: `produccion`, `desarrollo`, `test`, `manual`, `etl`, `reporte`

## 🛠️ Herramientas de Desarrollo

### Comandos Útiles (Makefile)

```bash
# Ver ayuda
make help

# Construir/reconstruir imagen
make build

# Iniciar servicios
make start

# Detener servicios
make stop

# Reiniciar servicios
make restart

# Ver logs
make logs

# Ver estado
make status

# Desplegar DAGs
make deploy
make deploy FILE=mi_dag.py

# Obtener password web
make get-password

# Limpiar todo
make clean
```

### Desarrollo Local

1. Editar DAGs en `dags_local/`
2. Desplegar con `make deploy`
3. Verificar en UI de Airflow
4. Revisar logs si hay errores
5. Iterar hasta que funcione

## 📖 Glosario

- **DAG** - Directed Acyclic Graph - Flujo de trabajo de Airflow
- **Task** - Unidad individual de trabajo dentro de un DAG
- **Operator** - Clase que define cómo ejecutar una tarea
- **Hook** - Interfaz para conectar con sistemas externos
- **Provider** - Paquete que contiene operators, hooks y sensors
- **Connection** - Configuración de credenciales para sistemas externos
- **XCom** - Mecanismo para compartir datos entre tareas
- **Schedule** - Programación de cuándo ejecutar un DAG
- **Catchup** - Ejecutar DAG runs históricos perdidos
- **Backfill** - Ejecutar manualmente DAG runs históricos

---

**Proyecto:** Airflow IDESA
**Versión:** 1.0.0
**Última actualización:** 2025-11-15
**Mantenido por:** Equipo de Desarrollo IDESA
