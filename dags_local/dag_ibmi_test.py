"""
DAG de prueba para consultar IBM i DB2 (AS/400) - Solo ejecución manual

Conexión IBM i DB2:
  Sistema: 192.168.24.1
  Usuario: WEBUSR
  Driver: iSeries Access ODBC Driver
  Biblioteca: QGPL

Para ejecutar este DAG:
  1. Ir a la UI de Airflow
  2. Buscar 'dag_ibmi_test'
  3. Hacer clic en el botón de "Play" para ejecutarlo manualmente
"""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.exceptions import AirflowException
import pyodbc

# Configuración de conexión
IBMI_SYSTEM = '192.168.24.1'
IBMI_USER = 'WEBUSR'
IBMI_PASSWORD = 'idesa18'
IBMI_DRIVER = 'iSeries Access ODBC Driver'

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

def verificar_driver_odbc():
    """Verifica que el driver ODBC esté disponible"""
    print("=" * 80)
    print("VERIFICANDO DRIVERS ODBC DISPONIBLES")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now()}")
    print("-" * 80)

    try:
        # Listar drivers ODBC disponibles
        drivers = pyodbc.drivers()
        print(f"Drivers ODBC encontrados: {len(drivers)}")
        print("-" * 80)

        for i, driver in enumerate(drivers, 1):
            print(f"{i}. {driver}")
            if 'iseries' in driver.lower() or 'db2' in driver.lower() or 'as400' in driver.lower():
                print(f"   ✓ Este driver puede usarse para IBM i")

        print("-" * 80)

        # Verificar si el driver específico está disponible
        if IBMI_DRIVER in drivers:
            print(f"✓ Driver '{IBMI_DRIVER}' encontrado")
        else:
            print(f"⚠ Driver '{IBMI_DRIVER}' NO encontrado")
            print(f"\nDrivers alternativos que podrían funcionar:")
            for driver in drivers:
                if 'iseries' in driver.lower() or 'db2' in driver.lower():
                    print(f"  - {driver}")

            if not any('iseries' in d.lower() or 'db2' in d.lower() for d in drivers):
                print("\n⚠ No se encontraron drivers compatibles con IBM i/DB2")
                print("\nPara instalar el driver, considera:")
                print("  1. IBM i Access ODBC Driver")
                print("  2. unixODBC + IBM i Access")
                print("  3. Configurar el driver en el Dockerfile")

        print("=" * 80)
        return True

    except Exception as e:
        error_msg = f"✗ Error al verificar drivers ODBC: {str(e)}"
        print(error_msg)
        print("=" * 80)
        raise AirflowException(error_msg)

def verificar_conexion_ibmi():
    """Verifica que la conexión a IBM i DB2 sea exitosa"""
    print("=" * 80)
    print("VERIFICANDO CONEXIÓN A IBM i DB2")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now()}")
    print(f"Sistema: {IBMI_SYSTEM}")
    print(f"Usuario: {IBMI_USER}")
    print(f"Driver: {IBMI_DRIVER}")
    print("-" * 80)

    try:
        # Intentar con el driver especificado
        connection_string = (
            f"DRIVER={{{IBMI_DRIVER}}};"
            f"SYSTEM={IBMI_SYSTEM};"
            f"UID={IBMI_USER};"
            f"PWD={IBMI_PASSWORD};"
            f"DefaultLibraries=QGPL;"
            f"ExtendedDynamic=1;"
            f"AllowDataCompression=1;"
            f"AllowUnsupportedChar=1;"
            f"ForceTranslation=1;"
            f"TrueAutoCommit=1;"
        )

        print(f"Intentando conectar a {IBMI_SYSTEM}...")
        print(f"String de conexión (sin password): DRIVER={{{IBMI_DRIVER}}};SYSTEM={IBMI_SYSTEM};UID={IBMI_USER};...")
        print("-" * 80)

        conn = pyodbc.connect(connection_string, timeout=10)
        print("✓ Conexión a IBM i DB2 exitosa")

        # Obtener información del sistema
        cursor = conn.cursor()

        # Obtener versión del sistema
        try:
            cursor.execute("SELECT OS_VERSION, OS_RELEASE FROM SYSIBMADM.ENV_SYS_INFO")
            row = cursor.fetchone()
            if row:
                print(f"✓ Versión OS: V{row[0]}R{row[1]}")
        except:
            print("⚠ No se pudo obtener versión del OS")

        # Obtener biblioteca actual
        try:
            cursor.execute("SELECT CURRENT SCHEMA FROM SYSIBM.SYSDUMMY1")
            row = cursor.fetchone()
            if row:
                print(f"✓ Esquema actual: {row[0]}")
        except:
            print("⚠ No se pudo obtener esquema actual")

        # Obtener usuario actual
        try:
            cursor.execute("SELECT USER FROM SYSIBM.SYSDUMMY1")
            row = cursor.fetchone()
            if row:
                print(f"✓ Usuario conectado: {row[0]}")
        except:
            print("⚠ No se pudo obtener usuario")

        cursor.close()
        conn.close()

        print("=" * 80)
        return True

    except pyodbc.Error as e:
        error_msg = f"✗ Error ODBC al conectar a IBM i: {str(e)}"
        print(error_msg)
        print("\nPosibles causas:")
        print("  - Driver ODBC no instalado o no disponible")
        print("  - Credenciales incorrectas")
        print("  - Sistema IBM i no accesible desde el contenedor")
        print("  - Firewall bloqueando la conexión")
        print("  - VPN requerida pero no activa")
        print("=" * 80)
        raise AirflowException(error_msg)
    except Exception as e:
        error_msg = f"✗ Error al verificar conexión: {str(e)}"
        print(error_msg)
        print("=" * 80)
        raise AirflowException(error_msg)

def consultar_tabla_ubitfra():
    """Consulta la tabla gxdbprueba.ubitfra y muestra los resultados"""
    print("=" * 80)
    print("CONSULTANDO TABLA gxdbprueba.ubitfra")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now()}")
    print("-" * 80)

    try:
        # Conectar a IBM i
        connection_string = (
            f"DRIVER={{{IBMI_DRIVER}}};"
            f"SYSTEM={IBMI_SYSTEM};"
            f"UID={IBMI_USER};"
            f"PWD={IBMI_PASSWORD};"
            f"DefaultLibraries=QGPL;"
            f"ExtendedDynamic=1;"
            f"AllowDataCompression=1;"
            f"AllowUnsupportedChar=1;"
            f"ForceTranslation=1;"
            f"TrueAutoCommit=1;"
        )

        conn = pyodbc.connect(connection_string, timeout=10)
        cursor = conn.cursor()

        # Ejecutar la consulta
        sql = "SELECT * FROM gxdbprueba.ubitfra FETCH FIRST 10 ROWS ONLY"

        print("Ejecutando consulta:")
        print(sql)
        print("-" * 80)

        cursor.execute(sql)

        # Obtener nombres de columnas
        columns = [column[0] for column in cursor.description]

        # Obtener los registros
        records = cursor.fetchall()

        print(f"✓ Consulta ejecutada exitosamente")
        print(f"✓ Registros encontrados: {len(records)}")
        print(f"✓ Columnas: {len(columns)}")
        print("-" * 80)

        if records:
            # Mostrar encabezados
            header_line = " | ".join(f"{col:20}" for col in columns)
            print(header_line)
            print("-" * len(header_line))

            # Mostrar los registros
            for i, record in enumerate(records, 1):
                row_data = []
                for value in record:
                    # Formatear el valor dependiendo del tipo
                    if value is None:
                        row_data.append("NULL")
                    elif isinstance(value, (datetime,)):
                        row_data.append(str(value))
                    elif isinstance(value, bytes):
                        try:
                            row_data.append(value.decode('utf-8', errors='ignore'))
                        except:
                            row_data.append(str(value))
                    else:
                        row_data.append(str(value))

                row_line = " | ".join(f"{str(val)[:20]:20}" for val in row_data)
                print(f"{row_line}")

            print("-" * 80)
            print(f"✓ Se mostraron {len(records)} registros")
        else:
            print("⚠ No se encontraron registros en la tabla gxdbprueba.ubitfra")

        cursor.close()
        conn.close()

        print("=" * 80)
        return len(records)

    except pyodbc.Error as e:
        error_msg = f"✗ Error ODBC al consultar la tabla: {str(e)}"
        print(error_msg)
        print("\nPosibles causas:")
        print("  - La tabla gxdbprueba.ubitfra no existe")
        print("  - El usuario no tiene permisos sobre la tabla")
        print("  - La biblioteca gxdbprueba no existe")
        print("  - Error en la sintaxis SQL")
        print("=" * 80)
        raise AirflowException(error_msg)
    except Exception as e:
        error_msg = f"✗ Error al consultar la tabla: {str(e)}"
        print(error_msg)
        print("=" * 80)
        raise AirflowException(error_msg)

def resumen_ejecucion(**context):
    """Muestra un resumen de la ejecución"""
    print("=" * 80)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 80)
    print(f"✓ DAG ejecutado manualmente: dag_ibmi_test")
    print(f"✓ Fecha y hora de ejecución: {datetime.now()}")
    print(f"✓ Sistema IBM i: {IBMI_SYSTEM}")
    print(f"✓ Conexión DB2: OK")
    print(f"✓ Consulta tabla ubitfra: OK")
    print("=" * 80)
    print("EJECUCIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)

# Definición del DAG
with DAG(
    'dag_ibmi_test',
    default_args=default_args,
    description='DAG de prueba para IBM i DB2 (AS/400) - Solo manual',
    schedule=None,  # Sin programación - solo ejecución manual
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['ibmi', 'db2', 'as400', 'test', 'manual'],
) as dag:

    # Tarea 1: Verificar drivers ODBC disponibles
    verificar_drivers = PythonOperator(
        task_id='verificar_driver_odbc',
        python_callable=verificar_driver_odbc,
    )

    # Tarea 2: Verificar conexión IBM i
    verificar_conexion = PythonOperator(
        task_id='verificar_conexion_ibmi',
        python_callable=verificar_conexion_ibmi,
    )

    # Tarea 3: Consultar tabla ubitfra
    consultar_ubitfra = PythonOperator(
        task_id='consultar_tabla_ubitfra',
        python_callable=consultar_tabla_ubitfra,
    )

    # Tarea 4: Resumen de ejecución
    mostrar_resumen = PythonOperator(
        task_id='resumen_ejecucion',
        python_callable=resumen_ejecucion,
    )

    # Definir el flujo de tareas
    verificar_drivers >> verificar_conexion >> consultar_ubitfra >> mostrar_resumen
