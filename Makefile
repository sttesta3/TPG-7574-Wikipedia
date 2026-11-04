SHELL := /bin/bash
PWD := $(shell pwd)

up:
	docker compose -f docker-compose.yaml build nodo-base
	mkdir -p output
	COMPOSE_HTTP_TIMEOUT=300 docker compose -f docker-compose.yaml up --build --remove-orphans --detach
	docker compose -f docker-compose.yaml logs --follow
.PHONY: up

down:
	docker compose -f docker-compose.yaml stop -t 5
	docker compose -f docker-compose.yaml down
.PHONY: down

logs:
	docker compose -f docker-compose.yaml logs
.PHONY: logs

test:
	docker compose -f docker-compose.yaml build nodo-base
	mkdir -p output
	rm ./output/* -f
	COMPOSE_HTTP_TIMEOUT=300 docker compose -f docker-compose.yaml up --build --remove-orphans --detach
	PYTHONPATH="$(PWD)/src/common" python3 ./verify_output.py; EXIT_CODE=$$?; \
	docker compose -f docker-compose.yaml stop -t 5; \
	docker compose -f docker-compose.yaml down; \
	exit $$EXIT_CODE
.PHONY: test

scenario:
	@read -p "Nombre del archivo de salida (ej. docker-compose-scenarioX.yaml): " archivo; \
	read -p "Cantidad de clientes: " cliente; \
	read -p "Cantidad de lote: " lote; \
	read -p "Cantidad de clasificadores: " clasif; \
	read -p "Cantidad de descargadores de imágenes: " imgDesc; \
	read -p "Cantidad de transformadores (transfor): " transfor; \
	read -p "Cantidad de promedio: " prom; \
	read -p "Cantidad de cuenta promedio: " contProm; \
	read -p "Cantidad de sum top: " sumTop; \
	read -p "Cantidad de agregador top : " agrTop; \
	read -p "Cantidad de join top : " joinTop; \
	bash generate_docker_compose.sh "$$archivo" "$$cliente" "$$lote" "$$clasif" "$$imgDesc" "$$transfor" "$$prom" "$$contProm" "$$sumTop" "$$agrTop" "$$joinTop"
.PHONY: build

switch:
	@read -p "Ingresar nombre de archivo a utilizar: " option;       \
	cp ./$${option} docker-compose.yaml

.PHONY: switch
