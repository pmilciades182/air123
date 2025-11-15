.PHONY: help build start stop restart logs clean status deploy

help:
	@echo "Comandos disponibles para Airflow:"
	@echo "  make build         - Construir las imágenes de Docker"
	@echo "  make start         - Iniciar Airflow (webserver + scheduler)"
	@echo "  make stop          - Detener todos los contenedores"
	@echo "  make restart       - Reiniciar Airflow"
	@echo "  make deploy        - Desplegar todos los DAGs de dags_local/ a dags/"
	@echo "  make deploy FILE=x - Desplegar solo el archivo especificado"
	@echo "  make logs          - Ver logs de todos los servicios"
	@echo "  make status        - Ver estado de los contenedores"
	@echo "  make clean         - Detener y eliminar contenedores, volúmenes"
	@echo ""
	@echo "Airflow UI: http://localhost:4000"
	@echo "Usuario: airflow / Contraseña: airflow"

build:
	@echo "Construyendo imágenes de Docker..."
	docker-compose build

start:
	@echo "Iniciando Airflow..."
	docker-compose up -d
	@echo ""
	@echo "Airflow iniciado correctamente!"
	@echo "Accede a la UI en: http://localhost:4000"
	@echo "Usuario: airflow"
	@echo "Contraseña: airflow"

stop:
	@echo "Deteniendo Airflow..."
	docker-compose down

restart: stop start

logs:
	docker-compose logs -f

logs-webserver:
	docker-compose logs -f airflow-webserver

logs-scheduler:
	docker-compose logs -f airflow-scheduler

status:
	docker-compose ps

clean:
	@echo "Limpiando contenedores y volúmenes..."
	docker-compose down -v
	@echo "Limpieza completada"

init:
	@echo "Inicializando proyecto..."
	mkdir -p dags logs plugins dags_local
	chmod 777 logs
	@echo "Proyecto inicializado"

deploy:
ifdef FILE
	@echo "Desplegando archivo: $(FILE)"
	@if [ ! -f dags_local/$(FILE) ]; then \
		echo "Error: El archivo dags_local/$(FILE) no existe"; \
		exit 1; \
	fi
	@SCHEDULER=$$(docker-compose ps -q airflow-scheduler 2>/dev/null); \
	if [ -z "$$SCHEDULER" ]; then \
		echo "Error: Airflow no está corriendo. Ejecuta 'make start' primero"; \
		exit 1; \
	fi; \
	docker cp dags_local/$(FILE) $$SCHEDULER:/opt/airflow/dags/$(FILE)
	@echo "Archivo desplegado correctamente"
	@echo "El DAG aparecerá en Airflow en ~30 segundos"
else
	@echo "Desplegando todos los DAGs de dags_local/ a dags/..."
	@if [ ! -d dags_local ]; then \
		echo "Error: La carpeta dags_local/ no existe"; \
		exit 1; \
	fi
	@if [ -z "$$(ls -A dags_local/*.py 2>/dev/null)" ]; then \
		echo "Advertencia: No hay archivos .py en dags_local/"; \
	else \
		SCHEDULER=$$(docker-compose ps -q airflow-scheduler 2>/dev/null); \
		if [ -z "$$SCHEDULER" ]; then \
			echo "Error: Airflow no está corriendo. Ejecuta 'make start' primero"; \
			exit 1; \
		fi; \
		for file in dags_local/*.py; do \
			filename=$$(basename $$file); \
			docker cp $$file $$SCHEDULER:/opt/airflow/dags/$$filename; \
			echo "Desplegado: $$filename"; \
		done; \
		echo ""; \
		echo "DAGs desplegados correctamente"; \
		echo "Los DAGs aparecerán en Airflow en ~30 segundos"; \
	fi
endif
