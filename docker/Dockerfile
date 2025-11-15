FROM apache/airflow:3.1.3-python3.13

USER root

# Instalar dependencias del sistema y ODBC
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
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

# Copiar requirements si existen
COPY docker/requirements.txt /requirements.txt
RUN chown airflow:root /requirements.txt

USER airflow

# Instalar dependencias de Python adicionales
RUN pip install --no-cache-dir -r /requirements.txt
