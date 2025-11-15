"""
DAG que envía un correo electrónico solo cuando se ejecuta manualmente
Este DAG no tiene programación automática (schedule=None)

Configuración SMTP requerida:
  Servidor: 192.168.250.30
  Puerto: 25
  Sin autenticación

Para ejecutar este DAG:
  1. Ir a la UI de Airflow
  2. Buscar 'dag_email_manual'
  3. Hacer clic en el botón de "Play" para ejecutarlo manualmente
"""
from datetime import datetime
import socket
import smtplib
from airflow import DAG
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.exceptions import AirflowException

# Configuración SMTP
SMTP_HOST = '192.168.250.30'
SMTP_PORT = 25

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

def verificar_conectividad_smtp():
    """Verifica que el servidor SMTP sea accesible"""
    print("=" * 60)
    print("VERIFICANDO CONECTIVIDAD SMTP")
    print("=" * 60)
    print(f"Servidor SMTP: {SMTP_HOST}")
    print(f"Puerto SMTP: {SMTP_PORT}")
    print(f"Fecha y hora: {datetime.now()}")
    print("-" * 60)

    # Verificar conectividad básica (TCP)
    try:
        print(f"Intentando conectar a {SMTP_HOST}:{SMTP_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # Timeout de 10 segundos
        resultado = sock.connect_ex((SMTP_HOST, SMTP_PORT))
        sock.close()

        if resultado == 0:
            print(f"✓ Conectividad TCP exitosa a {SMTP_HOST}:{SMTP_PORT}")
        else:
            error_msg = f"✗ No se puede conectar a {SMTP_HOST}:{SMTP_PORT} (código de error: {resultado})"
            print(error_msg)
            print("\nPosibles causas:")
            print("  - Firewall bloqueando el puerto 25")
            print("  - VPN no permite acceso a esta red")
            print("  - Servidor SMTP no está corriendo")
            print("  - IP o puerto incorrectos")
            raise AirflowException(error_msg)

    except socket.timeout:
        error_msg = f"✗ Timeout al intentar conectar a {SMTP_HOST}:{SMTP_PORT}"
        print(error_msg)
        print("\nEl servidor no respondió en 10 segundos")
        raise AirflowException(error_msg)
    except Exception as e:
        error_msg = f"✗ Error al verificar conectividad: {str(e)}"
        print(error_msg)
        raise AirflowException(error_msg)

    # Verificar protocolo SMTP
    try:
        print(f"Verificando protocolo SMTP...")
        smtp = smtplib.SMTP(timeout=10)
        smtp.connect(SMTP_HOST, SMTP_PORT)
        print(f"✓ Conexión SMTP exitosa")
        print(f"Servidor responde: {smtp.ehlo_resp.decode() if smtp.ehlo_resp else 'N/A'}")
        smtp.quit()
        print("=" * 60)
        return True
    except Exception as e:
        error_msg = f"✗ Error en protocolo SMTP: {str(e)}"
        print(error_msg)
        raise AirflowException(error_msg)

def log_ejecucion_manual():
    """Registra que el DAG fue ejecutado manualmente"""
    print("=" * 60)
    print("DAG EJECUTADO MANUALMENTE")
    print("=" * 60)
    print(f"Fecha y hora: {datetime.now()}")
    print(f"Servidor SMTP: {SMTP_HOST}:{SMTP_PORT}")
    print("Preparando para enviar correo electrónico...")
    print("=" * 60)

# Definición del DAG
with DAG(
    'dag_email_manual',
    default_args=default_args,
    description='DAG que envía email solo cuando se ejecuta manualmente',
    schedule=None,  # Sin programación - solo ejecución manual
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['email', 'manual'],
) as dag:

    # Tarea 1: Log de ejecución manual
    log_inicio = PythonOperator(
        task_id='log_ejecucion_manual',
        python_callable=log_ejecucion_manual,
    )

    # Tarea 2: Verificar conectividad SMTP
    verificar_smtp = PythonOperator(
        task_id='verificar_conectividad_smtp',
        python_callable=verificar_conectividad_smtp,
    )

    # Tarea 3: Enviar correo electrónico
    enviar_email = EmailOperator(
        task_id='enviar_email',
        to='pablo.gonzalez@idesa.com.py',
        subject='test',
        html_content='test',
        conn_id='smtp_idesa',  # Conexión SMTP configurada en variables de entorno
    )

    # Definir el flujo de tareas
    log_inicio >> verificar_smtp >> enviar_email
