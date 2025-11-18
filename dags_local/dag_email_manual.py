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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow import DAG
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

def enviar_email_sin_ssl():
    """Envía un email usando SMTP sin SSL/TLS"""
    print("=" * 60)
    print("ENVIANDO EMAIL")
    print("=" * 60)

    destinatario = 'pablo.gonzalez@idesa.com.py'
    remitente = 'airflow@idesa.com.py'
    asunto = 'Test desde Airflow - Ejecución Manual'

    # Crear el mensaje
    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = asunto
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    # Contenido HTML del email
    html_content = f"""
    <html>
      <head></head>
      <body>
        <h2>Test de Email desde Airflow</h2>
        <p>Este es un email de prueba enviado desde Airflow.</p>
        <p><strong>Fecha y hora de ejecución:</strong> {datetime.now()}</p>
        <p><strong>Servidor SMTP:</strong> {SMTP_HOST}:{SMTP_PORT}</p>
        <p><strong>Estado:</strong> Email enviado exitosamente sin SSL/TLS</p>
      </body>
    </html>
    """

    parte_html = MIMEText(html_content, 'html')
    mensaje.attach(parte_html)

    try:
        print(f"Conectando a servidor SMTP {SMTP_HOST}:{SMTP_PORT} sin SSL...")
        # Conectar sin SSL
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)

        print(f"Enviando email desde {remitente} a {destinatario}...")
        smtp.sendmail(remitente, destinatario, mensaje.as_string())

        print(f"✓ Email enviado exitosamente a {destinatario}")
        smtp.quit()
        print("=" * 60)

    except Exception as e:
        error_msg = f"✗ Error al enviar email: {str(e)}"
        print(error_msg)
        raise AirflowException(error_msg)

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

    # Tarea 3: Enviar correo electrónico (usando función personalizada sin SSL)
    enviar_email = PythonOperator(
        task_id='enviar_email',
        python_callable=enviar_email_sin_ssl,
    )

    # Definir el flujo de tareas
    log_inicio >> verificar_smtp >> enviar_email
