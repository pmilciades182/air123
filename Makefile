.PHONY: help build start stop restart logs clean status deploy setup-local

# Cargar PROJECT_NAME del archivo .env
include .env
export

# Comando base de docker-compose con nombre de proyecto
DOCKER_COMPOSE = docker-compose --project-name $(PROJECT_NAME)

help:
	@echo "Comandos disponibles para Airflow (Instancia: $(PROJECT_NAME)):"
	@echo ""
	@echo "Desarrollo:"
	@echo "  make setup-local   - Configurar entorno local para VS Code (IntelliSense)"
	@echo ""
	@echo "Docker/Airflow:"
	@echo "  make build         - Construir las imágenes de Docker"
	@echo "  make start         - Iniciar Airflow (webserver + scheduler)"
	@echo "  make stop          - Detener todos los contenedores"
	@echo "  make restart       - Reiniciar Airflow"
	@echo "  make deploy        - Desplegar todos los DAGs de dags_local/ a dags/"
	@echo "  make deploy FILE=x - Desplegar solo el archivo especificado"
	@echo "  make get-password  - Obtener contraseña de Airflow (Airflow 3.x)"
	@echo "  make logs          - Ver logs de todos los servicios"
	@echo "  make status        - Ver estado de los contenedores"
	@echo "  make clean         - Detener y eliminar contenedores, volúmenes"
	@echo ""
	@echo "Instancia actual: $(PROJECT_NAME)"
	@echo "Airflow UI: http://localhost:$(AIRFLOW_WEBSERVER_PORT)"
	@echo "Usuario: $(AIRFLOW_WWW_USER_USERNAME) / Contraseña: usar 'make get-password'"

build:
	@echo "Construyendo imágenes de Docker para $(PROJECT_NAME)..."
	$(DOCKER_COMPOSE) build

start:
	@echo "Iniciando Airflow ($(PROJECT_NAME))..."
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "Airflow iniciado correctamente!"
	@echo "Instancia: $(PROJECT_NAME)"
	@echo "Accede a la UI en: http://localhost:$(AIRFLOW_WEBSERVER_PORT)"
	@echo "Usuario: $(AIRFLOW_WWW_USER_USERNAME)"
	@echo "Contraseña: usar 'make get-password'"

stop:
	@echo "Deteniendo Airflow ($(PROJECT_NAME))..."
	$(DOCKER_COMPOSE) down

restart: stop start

logs:
	$(DOCKER_COMPOSE) logs -f

logs-webserver:
	$(DOCKER_COMPOSE) logs -f airflow-webserver

logs-scheduler:
	$(DOCKER_COMPOSE) logs -f airflow-scheduler

get-password:
	@echo "Obteniendo contraseña de Airflow ($(PROJECT_NAME))..."
	@$(DOCKER_COMPOSE) logs airflow-webserver 2>&1 | grep "Password for user" | tail -1 || echo "Airflow aún no ha generado la contraseña. Espera unos segundos y vuelve a intentar."

status:
	$(DOCKER_COMPOSE) ps

clean:
	@echo "Limpiando contenedores y volúmenes de $(PROJECT_NAME)..."
	$(DOCKER_COMPOSE) down -v
	@echo "Limpieza completada"

init:
	@echo "Inicializando proyecto $(PROJECT_NAME)..."
	mkdir -p dags logs plugins dags_local
	chmod 777 logs
	@echo "Proyecto inicializado"

deploy:
ifdef FILE
	@echo "Desplegando archivo: $(FILE) (Instancia: $(PROJECT_NAME))"
	@if [ ! -f dags_local/$(FILE) ]; then \
		echo "Error: El archivo dags_local/$(FILE) no existe"; \
		exit 1; \
	fi
	@SCHEDULER=$$($(DOCKER_COMPOSE) ps -q airflow-scheduler 2>/dev/null); \
	if [ -z "$$SCHEDULER" ]; then \
		echo "Error: Airflow no está corriendo. Ejecuta 'make start' primero"; \
		exit 1; \
	fi; \
	docker cp dags_local/$(FILE) $$SCHEDULER:/opt/airflow/dags/$(FILE); \
	$(DOCKER_COMPOSE) exec -T --user root airflow-scheduler chmod 644 /opt/airflow/dags/$(FILE); \
	$(DOCKER_COMPOSE) exec -T --user root airflow-scheduler chown airflow:root /opt/airflow/dags/$(FILE)
	@echo "Archivo desplegado correctamente"
	@echo "El DAG aparecerá en Airflow en ~30 segundos"
else
	@echo "Desplegando todos los DAGs de dags_local/ a dags/ ($(PROJECT_NAME))..."
	@if [ ! -d dags_local ]; then \
		echo "Error: La carpeta dags_local/ no existe"; \
		exit 1; \
	fi
	@if [ -z "$$(ls -A dags_local/*.py 2>/dev/null)" ]; then \
		echo "Advertencia: No hay archivos .py en dags_local/"; \
	else \
		SCHEDULER=$$($(DOCKER_COMPOSE) ps -q airflow-scheduler 2>/dev/null); \
		if [ -z "$$SCHEDULER" ]; then \
			echo "Error: Airflow no está corriendo. Ejecuta 'make start' primero"; \
			exit 1; \
		fi; \
		for file in dags_local/*.py; do \
			filename=$$(basename $$file); \
			docker cp $$file $$SCHEDULER:/opt/airflow/dags/$$filename; \
			$(DOCKER_COMPOSE) exec -T --user root airflow-scheduler chmod 644 /opt/airflow/dags/$$filename; \
			$(DOCKER_COMPOSE) exec -T --user root airflow-scheduler chown airflow:root /opt/airflow/dags/$$filename; \
			echo "Desplegado: $$filename"; \
		done; \
		echo ""; \
		echo "DAGs desplegados correctamente"; \
		echo "Los DAGs aparecerán en Airflow en ~30 segundos"; \
	fi
endif

setup-local:
	@echo "========================================="
	@echo "Configurando entorno local para VS Code"
	@echo "========================================="
	@echo ""
	@echo "Este comando configurará:"
	@echo "  - Entorno virtual Python (.venv)"
	@echo "  - Dependencias de Airflow para IntelliSense"
	@echo "  - Configuración de VS Code"
	@echo ""
	@# Verificar que python3 esté instalado
	@if ! command -v python3 >/dev/null 2>&1; then \
		echo "❌ Error: python3 no está instalado"; \
		echo "Instala Python 3.13 o superior primero"; \
		exit 1; \
	fi
	@# Mostrar versión de Python
	@echo "Versión de Python detectada: $$(python3 --version)"
	@echo ""
	@# Crear entorno virtual si no existe
	@if [ ! -d .venv ]; then \
		echo "📦 Creando entorno virtual..."; \
		python3 -m venv .venv; \
		echo "✅ Entorno virtual creado"; \
	else \
		echo "✅ Entorno virtual ya existe"; \
	fi
	@echo ""
	@# Actualizar pip
	@echo "⬆️  Actualizando pip..."
	@.venv/bin/pip install --quiet --upgrade pip
	@echo "✅ pip actualizado"
	@echo ""
	@# Instalar dependencias
	@echo "📥 Instalando dependencias de Airflow (esto puede tardar unos minutos)..."
	@.venv/bin/pip install --quiet apache-airflow==3.1.3
	@.venv/bin/pip install --quiet apache-airflow-providers-standard
	@.venv/bin/pip install --quiet -r docker/requirements.txt
	@echo "✅ Dependencias instaladas"
	@echo ""
	@# Crear carpeta .vscode si no existe
	@mkdir -p .vscode
	@# Verificar configuración de VS Code
	@if [ -f .vscode/settings.json ]; then \
		echo "✅ Configuración de VS Code ya existe"; \
	else \
		echo "⚠️  Advertencia: .vscode/settings.json no encontrado"; \
		echo "   Debería haber sido creado automáticamente"; \
	fi
	@echo ""
	@echo "========================================="
	@echo "✅ Configuración completada exitosamente"
	@echo "========================================="
	@echo ""
	@echo "Próximos pasos:"
	@echo ""
	@echo "1. Recarga VS Code (o cierra y abre el proyecto nuevamente)"
	@echo ""
	@echo "2. Selecciona el intérprete de Python:"
	@echo "   - Presiona Ctrl+Shift+P"
	@echo "   - Escribe 'Python: Select Interpreter'"
	@echo "   - Selecciona el que dice '.venv' o './venv/bin/python'"
	@echo ""
	@echo "3. Verifica que los imports ya no muestren errores en dags_local/"
	@echo ""
	@echo "Nota: El entorno .venv es SOLO para VS Code IntelliSense."
	@echo "      Airflow sigue ejecutándose en Docker con sus propias dependencias."
	@echo ""
