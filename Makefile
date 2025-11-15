.PHONY: help build start stop restart logs clean status

help:
	@echo "Comandos disponibles para Airflow:"
	@echo "  make build    - Construir las imágenes de Docker"
	@echo "  make start    - Iniciar Airflow (webserver + scheduler)"
	@echo "  make stop     - Detener todos los contenedores"
	@echo "  make restart  - Reiniciar Airflow"
	@echo "  make logs     - Ver logs de todos los servicios"
	@echo "  make status   - Ver estado de los contenedores"
	@echo "  make clean    - Detener y eliminar contenedores, volúmenes"
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
	mkdir -p dags logs plugins
	chmod 777 logs
	@echo "Proyecto inicializado"
