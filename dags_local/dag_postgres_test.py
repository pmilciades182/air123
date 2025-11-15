"""
DAG de prueba para consultar PostgreSQL (solo ejecución manual)

Conexión PostgreSQL:
  Host: 192.168.24.109
  Puerto: 5433
  Base de datos: planos
  Usuario: postgres

Para ejecutar este DAG:
  1. Ir a la UI de Airflow
  2. Buscar 'dag_postgres_test'
  3. Hacer clic en el botón de "Play" para ejecutarlo manualmente
"""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowException

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

def verificar_conexion_postgres():
    """Verifica que la conexión a PostgreSQL sea exitosa"""
    print("=" * 80)
    print("VERIFICANDO CONEXIÓN A POSTGRESQL")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now()}")
    print(f"Connection ID: postgres_idesa")
    print("-" * 80)

    try:
        # Crear el hook de PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='postgres_idesa')

        # Obtener la conexión
        conn = pg_hook.get_conn()
        print("✓ Conexión a PostgreSQL exitosa")

        # Obtener información del servidor
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ Versión de PostgreSQL: {version}")

        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        print(f"✓ Base de datos actual: {db_name}")

        cursor.execute("SELECT current_user;")
        user = cursor.fetchone()[0]
        print(f"✓ Usuario actual: {user}")

        cursor.close()
        conn.close()

        print("=" * 80)
        return True

    except Exception as e:
        error_msg = f"✗ Error al conectar a PostgreSQL: {str(e)}"
        print(error_msg)
        print("\nPosibles causas:")
        print("  - Credenciales incorrectas")
        print("  - Base de datos no existe")
        print("  - Firewall bloqueando el puerto 5433")
        print("  - VPN no permite acceso a esta red")
        print("=" * 80)
        raise AirflowException(error_msg)

def consultar_tabla_fraccion():
    """Consulta la tabla FRACCION y muestra los resultados"""
    print("=" * 80)
    print("CONSULTANDO TABLA FRACCION")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now()}")
    print("-" * 80)

    try:
        # Crear el hook de PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='postgres_idesa')

        # Ejecutar la consulta
        sql = """
        SELECT nfrac, centro_f, fecha, hora, usuario, estado
        FROM public."FRACCION"
        LIMIT 10;
        """

        print("Ejecutando consulta:")
        print(sql)
        print("-" * 80)

        # Obtener los resultados
        records = pg_hook.get_records(sql)

        print(f"✓ Consulta ejecutada exitosamente")
        print(f"✓ Registros encontrados: {len(records)}")
        print("-" * 80)

        if records:
            # Mostrar encabezados
            headers = ['nfrac', 'centro_f', 'fecha', 'hora', 'usuario', 'estado']
            header_line = " | ".join(f"{h:15}" for h in headers)
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
                    else:
                        row_data.append(str(value))

                row_line = " | ".join(f"{val:15}" for val in row_data)
                print(f"{row_line}")

            print("-" * 80)
            print(f"✓ Se mostraron {len(records)} registros")
        else:
            print("⚠ No se encontraron registros en la tabla FRACCION")

        print("=" * 80)
        return len(records)

    except Exception as e:
        error_msg = f"✗ Error al consultar la tabla: {str(e)}"
        print(error_msg)
        print("\nPosibles causas:")
        print("  - La tabla FRACCION no existe")
        print("  - El usuario no tiene permisos sobre la tabla")
        print("  - El esquema 'public' no existe")
        print("  - Error en la sintaxis SQL")
        print("=" * 80)
        raise AirflowException(error_msg)

def resumen_ejecucion(**context):
    """Muestra un resumen de la ejecución"""
    print("=" * 80)
    print("RESUMEN DE EJECUCIÓN")
    print("=" * 80)
    print(f"✓ DAG ejecutado manualmente: dag_postgres_test")
    print(f"✓ Fecha y hora de ejecución: {datetime.now()}")
    print(f"✓ Conexión PostgreSQL: OK")
    print(f"✓ Consulta tabla FRACCION: OK")
    print("=" * 80)
    print("EJECUCIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)

# Definición del DAG
with DAG(
    'dag_postgres_test',
    default_args=default_args,
    description='DAG de prueba para consultar PostgreSQL (solo manual)',
    schedule=None,  # Sin programación - solo ejecución manual
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['postgres', 'test', 'manual'],
) as dag:

    # Tarea 1: Verificar conexión PostgreSQL
    verificar_conexion = PythonOperator(
        task_id='verificar_conexion_postgres',
        python_callable=verificar_conexion_postgres,
    )

    # Tarea 2: Consultar tabla FRACCION
    consultar_fraccion = PythonOperator(
        task_id='consultar_tabla_fraccion',
        python_callable=consultar_tabla_fraccion,
    )

    # Tarea 3: Resumen de ejecución
    mostrar_resumen = PythonOperator(
        task_id='resumen_ejecucion',
        python_callable=resumen_ejecucion,
    )

    # Definir el flujo de tareas
    verificar_conexion >> consultar_fraccion >> mostrar_resumen
