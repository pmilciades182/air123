FROM apache/airflow:2.10.4-python3.11

USER root

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements si existen
COPY docker/requirements.txt /requirements.txt
RUN chown airflow:root /requirements.txt

USER airflow

# Instalar dependencias de Python adicionales
RUN pip install --no-cache-dir -r /requirements.txt
