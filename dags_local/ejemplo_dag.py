"""
DAG de ejemplo para demostrar Airflow
Este DAG ejecuta tareas simples cada día a las 8:00 AM

Para desplegar este DAG:
  make deploy
  # O para desplegar un archivo específico:
  make deploy FILE=ejemplo_dag.py
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Funciones Python de ejemplo
def tarea_inicio():
    """Tarea de inicio del flujo"""
    print("Iniciando el flujo de trabajo...")
    print(f"Fecha de ejecución: {datetime.now()}")
    return "Flujo iniciado correctamente"

def procesar_datos():
    """Simula procesamiento de datos"""
    print("Procesando datos...")
    datos = [1, 2, 3, 4, 5]
    resultado = sum(datos)
    print(f"Resultado del procesamiento: {resultado}")
    return resultado

def finalizar():
    """Tarea final del flujo"""
    print("Finalizando el flujo de trabajo...")
    print("Todas las tareas completadas exitosamente")
    return "Flujo finalizado"

# Definición del DAG
with DAG(
    'ejemplo_dag',
    default_args=default_args,
    description='DAG de ejemplo con tareas básicas',
    schedule='0 8 * * *',  # Ejecutar diariamente a las 8:00 AM (Airflow 3.x usa 'schedule' en lugar de 'schedule_interval')
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['ejemplo', 'tutorial'],
) as dag:

    # Tarea 1: Inicio
    inicio = PythonOperator(
        task_id='inicio',
        python_callable=tarea_inicio,
    )

    # Tarea 2: Comando Bash
    verificar_sistema = BashOperator(
        task_id='verificar_sistema',
        bash_command='echo "Sistema: $(uname -a)" && echo "Fecha: $(date)"',
    )

    # Tarea 3: Procesamiento
    procesamiento = PythonOperator(
        task_id='procesar_datos',
        python_callable=procesar_datos,
    )

    # Tarea 4: Finalización
    fin = PythonOperator(
        task_id='finalizar',
        python_callable=finalizar,
    )

    # Definir el flujo de tareas (dependencias)
    inicio >> verificar_sistema >> procesamiento >> fin
