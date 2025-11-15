#!/bin/bash
# ==============================================================================
# Script para generar claves de seguridad de Airflow
# ==============================================================================
# Este script genera todas las claves necesarias para configurar Airflow
#
# Uso:
#   chmod +x generate-keys.sh
#   ./generate-keys.sh
# ==============================================================================

echo "=================================================="
echo "Generador de Claves de Seguridad para Airflow"
echo "=================================================="
echo ""

# Generar Fernet Key
echo "1. Generando AIRFLOW_FERNET_KEY..."
FERNET_KEY=$(docker run --rm apache/airflow:3.1.3-python3.13 python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 2>/dev/null)

if [ -z "$FERNET_KEY" ]; then
    echo "   ⚠️  No se pudo generar con Docker. Intentando con Python local..."
    FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 2>/dev/null)

    if [ -z "$FERNET_KEY" ]; then
        echo "   ❌ Error: No se pudo generar FERNET_KEY"
        echo "   Instala cryptography: pip install cryptography"
        FERNET_KEY="ERROR_INSTALAR_CRYPTOGRAPHY"
    else
        echo "   ✅ Generada exitosamente"
    fi
else
    echo "   ✅ Generada exitosamente"
fi

# Generar JWT Secret
echo ""
echo "2. Generando AIRFLOW_JWT_SECRET..."
JWT_SECRET=$(openssl rand -base64 16 2>/dev/null)

if [ -z "$JWT_SECRET" ]; then
    echo "   ❌ Error: No se pudo generar JWT_SECRET"
    echo "   Instala OpenSSL"
    JWT_SECRET="ERROR_INSTALAR_OPENSSL"
else
    echo "   ✅ Generada exitosamente"
fi

# Generar Internal API Secret
echo ""
echo "3. Generando AIRFLOW_INTERNAL_API_SECRET..."
INTERNAL_SECRET="airflow-internal-$(openssl rand -hex 8 2>/dev/null)"
if [ -z "$INTERNAL_SECRET" ]; then
    INTERNAL_SECRET="airflow-internal-api-secret-$(date +%s)"
fi
echo "   ✅ Generada exitosamente"

# Mostrar resultados
echo ""
echo "=================================================="
echo "Claves Generadas - Copia estos valores a tu .env"
echo "=================================================="
echo ""
echo "AIRFLOW_FERNET_KEY=$FERNET_KEY"
echo "AIRFLOW_JWT_SECRET=$JWT_SECRET"
echo "AIRFLOW_INTERNAL_API_SECRET=$INTERNAL_SECRET"
echo ""
echo "=================================================="
echo ""

# Ofrecer crear archivo .env
read -p "¿Deseas que se agreguen estas claves a un archivo .env? (s/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[SsYy]$ ]]; then
    if [ -f ".env" ]; then
        echo "⚠️  Ya existe un archivo .env"
        read -p "¿Deseas crear un respaldo (.env.backup) y actualizar? (s/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[SsYy]$ ]]; then
            cp .env .env.backup
            echo "✅ Respaldo creado: .env.backup"

            # Actualizar claves en .env existente
            sed -i "s|^AIRFLOW_FERNET_KEY=.*|AIRFLOW_FERNET_KEY=$FERNET_KEY|" .env
            sed -i "s|^AIRFLOW_JWT_SECRET=.*|AIRFLOW_JWT_SECRET=$JWT_SECRET|" .env
            sed -i "s|^AIRFLOW_INTERNAL_API_SECRET=.*|AIRFLOW_INTERNAL_API_SECRET=$INTERNAL_SECRET|" .env

            echo "✅ Claves actualizadas en .env"
        else
            echo "❌ Operación cancelada"
        fi
    else
        # Crear nuevo .env desde .env.example.local
        if [ -f ".env.example.local" ]; then
            cp .env.example.local .env

            # Reemplazar placeholders con claves generadas
            sed -i "s|AIRFLOW_FERNET_KEY=.*|AIRFLOW_FERNET_KEY=$FERNET_KEY|" .env
            sed -i "s|AIRFLOW_JWT_SECRET=.*|AIRFLOW_JWT_SECRET=$JWT_SECRET|" .env
            sed -i "s|AIRFLOW_INTERNAL_API_SECRET=.*|AIRFLOW_INTERNAL_API_SECRET=$INTERNAL_SECRET|" .env

            echo "✅ Archivo .env creado desde .env.example.local con las claves generadas"
            echo ""
            echo "⚠️  IMPORTANTE: Revisa y ajusta las siguientes variables en .env:"
            echo "   - PROJECT_NAME"
            echo "   - POSTGRES_HOST"
            echo "   - POSTGRES_PORT"
            echo "   - POSTGRES_DB"
            echo "   - POSTGRES_USER"
            echo "   - POSTGRES_PASSWORD"
            echo "   - AIRFLOW_WEBSERVER_PORT"
        else
            echo "❌ No se encontró .env.example.local"
            echo "   Copia manualmente las claves mostradas arriba a tu .env"
        fi
    fi
else
    echo "ℹ️  Copia manualmente las claves mostradas arriba a tu archivo .env"
fi

echo ""
echo "=================================================="
echo "Siguiente paso:"
echo "=================================================="
echo "1. Verifica la configuración en .env"
echo "2. Crea la base de datos en PostgreSQL"
echo "3. Ejecuta: make build && make start"
echo ""
