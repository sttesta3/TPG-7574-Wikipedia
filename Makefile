SHELL := /bin/bash
PWD := $(shell pwd)
COMPOSE ?= docker-compose.yaml
DC := docker compose --project-directory $(PWD) -f $(COMPOSE)

up:
	$(DC) build nodo-base
	mkdir -p output
	COMPOSE_HTTP_TIMEOUT=300 $(DC) up --build --remove-orphans --detach
	$(DC) logs --follow
.PHONY: up

down:
	$(DC) stop -t 5
	$(DC) down
.PHONY: down

logs:
	$(DC) logs
.PHONY: logs

test:
	$(DC) build nodo-base
	mkdir -p output
	rm ./output/* -f
	COMPOSE_HTTP_TIMEOUT=300 $(DC) up --build --remove-orphans --detach
	PYTHONPATH="$(PWD)/src/common" python3 ./verify_output.py; EXIT_CODE=$$?; \
	$(DC) stop -t 5; \
	$(DC) down; \
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
.PHONY: scenario

switch:
	@read -p "Ingresar nombre de archivo a utilizar: " option;       \
	cp ./$${option} docker-compose.yaml

.PHONY: switch

# Demo: 1) una instancia de cada worker y un cliente  2) workers escalados y varios clientes
demo-clean:
	mkdir -p output
	docker run --rm -v $(PWD)/output:/output --entrypoint sh nodo-base:latest -c 'rm -f /output/*'
.PHONY: demo-clean

demo-1: demo-clean
	$(MAKE) up COMPOSE=scenarios/demo-1.yaml
.PHONY: demo-1

demo-escalado: demo-clean
	$(MAKE) up COMPOSE=scenarios/demo-escalado.yaml
.PHONY: demo-escalado

demo-down:
	-$(MAKE) down COMPOSE=scenarios/demo-1.yaml
	-$(MAKE) down COMPOSE=scenarios/demo-escalado.yaml
.PHONY: demo-down
