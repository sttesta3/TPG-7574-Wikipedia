#!/bin/bash

if [[ $# -ne 11 ]]; then
	echo "Usage: $0 <nombre-compose> <clientes> <lote> <clasif> <imgDesc> <transfor> <prom> <contProm> <sumTop> <agrTop> <joinTop>"
	exit 1
fi 

for arg in "${@:2}"; do
        if [[ ! $arg =~ ^[0-9]+$ ]]; then
                echo "Todos los argumentos deben ser numéricos y positivos"
                exit 1
        elif [[ $arg -lt 1 ]]; then
                echo "Todos los argumentos deben ser mayores o iguales a 1"
                exit 1
        fi
done

archivo_salida=$1
clientes=$2
lote=$3
cant_clasif=$4
cant_descarg=$5
cant_transf=$6
cant_promedio=$7
cant_cuenta_promedio=$8
cant_sum_top=$9
cant_agr_top=${10}
cant_join_top=${11}

# Cantidad de parquets por idioma que lee cada cliente (opcional, por entorno)
datasets_en=${DATASETS_EN:-5}
datasets_fr=${DATASETS_FR:-5}
datasets_distintos=${DATASETS_DISTINTOS:-0}

descargas_por_minuto=${DESCARGAS_POR_MINUTO:-150}
descargas_por_minuto_nodo=$(( descargas_por_minuto / cant_descarg ))
(( descargas_por_minuto_nodo < 1 )) && descargas_por_minuto_nodo=1

CLASIFICADOR="clasificador"
TRANSFORMADOR="transformador"

definicion_base() {
	local nombre=$1
	local indice=$2
	local carpeta=$3
	echo "
  ${nombre}_$indice:
    build:
      context: ./src/
      dockerfile: $carpeta/Dockerfile
    container_name: ${nombre}_$indice
    depends_on:" >> $archivo_salida
}

agregar_dependencias_comunes() {
	echo "        rabbitmq:
          condition: service_healthy
        gateway:
          condition: service_started
        nodo-base:
          condition: service_started" >> $archivo_salida
}

agregar_dependencia() {
        local nombre=$1
        local cant=$2
 	for ((j=0; j<$cant; j++)); do echo "        ${nombre}_$j:
          condition: service_started" >> $archivo_salida
	done
}

echo "services:
  nodo-base:
      build:
        context: ./src/
        dockerfile: base/Dockerfile
      image: nodo-base:latest

  gateway:
    build:
      context: ./src/
      dockerfile: gateway/Dockerfile
    container_name: gateway
    depends_on:
      rabbitmq:
        condition: service_healthy
    environment:
      - PYTHONUNBUFFERED=1
      - GATEWAYHOST=gateway
      - GATEWAYPORT=8000
      - MOMHOST=rabbitmq
      - COLADATOS=EntradaDatos
      - COLARESPUESTAS=Respuestas
      - LOTE=$lote
      - TOTALCLASIFEOF=$cant_clasif
      - TOTALIMGEOF=$cant_descarg
      - TOTALAGRTOPEOF=$cant_agr_top
      - TOTALTOPEOF=1
      - TOTALCUENTAPROMEOF=$cant_cuenta_promedio
    healthcheck:
      test: ['CMD', 'python3', '-c', \"import socket; s=socket.create_connection(('127.0.0.1', 8000), timeout=2); s.close()\"]
      interval: 2s
      timeout: 3s
      retries: 15
      start_period: 5s

  rabbitmq:
      build:
        context: ./src/middleware
        dockerfile: Dockerfile
      container_name: rabbitmq
      environment:
      - RABBITMQ_LOG_LEVELS=error
      healthcheck:
        interval: 5s
        retries: 3
        start_period: 120s
        test: rabbitmq-diagnostics check_port_connectivity
        timeout: 3s
      ports:
      - 5672:5672
      - 15672:15672" > $archivo_salida

for ((i=0; i<$clientes; i++)); do 
	definicion_base "cliente" $i "cliente"
	echo "      gateway:
        condition: service_healthy
    environment:
    - DATASETPATHEN=/datasets/enwiki_namespace_0_
    - DATASETPATHFR=/datasets/frwiki_namespace_0_
    - TOTALDATASETSEN=$datasets_en
    - TOTALDATASETSFR=$datasets_fr
    - GATEWAYHOST=gateway
    - GATEWAYPORT=8000
    - LOTE=$lote
    - PYTHONUNBUFFERED=1
    - ID=$i
    - DATASETINICIO=$(( datasets_distintos ? i * (datasets_en > datasets_fr ? datasets_en : datasets_fr) : 0 ))
    volumes:
    - ./datasets:/datasets
    - ./output:/output" >> $archivo_salida 
done

for ((i=0; i<$cant_clasif; i++)); do 
	definicion_base $CLASIFICADOR $i $CLASIFICADOR
	agregar_dependencias_comunes
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLADATOS=EntradaDatos
      - COLARESPUESTAS=Respuestas
      - COLAIMGDESCARGA=ImgDescarga
      - COLATRANSFORMADOR=ColaTransformador
      - CLASIFICADOREXCHANGEEOF=ClasificadorExchangeEof" >> $archivo_salida
done

for ((i=0; i<$cant_descarg; i++)); do 
	definicion_base "img_descargador" $i "imgDescargador" 
	agregar_dependencias_comunes
	agregar_dependencia $CLASIFICADOR $cant_clasif
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLARESPUESTAS=Respuestas
      - COLAIMGDESCARGA=ImgDescarga
      - EXCHANGEIMGEOF=ExchangeImgEof
      - MAXCLIENTES=1
      - DESCARGASPORMINUTO=$descargas_por_minuto_nodo" >> $archivo_salida
done

for ((i=0; i<$cant_transf; i++)); do 
	definicion_base $TRANSFORMADOR $i $TRANSFORMADOR
	agregar_dependencias_comunes
	agregar_dependencia $CLASIFICADOR $cant_clasif	
 	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLATRANSFORMADOR=ColaTransformador
      - COLASUMTOP=ColaSumTop
      - EXCHANGEPROMEDIO=ExchangePromedio
      - COLACUENTAPROM=ColaCuentaProm
      - EXCHANGETRANSFORMADOREOF=ExchangeTransformadorEof
      - TOTALCUENTAPROM=$cant_cuenta_promedio
      - TOTALPROMEDIO=$cant_promedio" >> $archivo_salida
done 

for ((i=0; i<$cant_promedio; i++)); do 
	definicion_base "promedio" $i "promedio" 
	agregar_dependencias_comunes
        agregar_dependencia $CLASIFICADOR $cant_clasif
 	agregar_dependencia $TRANSFORMADOR $cant_transf
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLACUENTAPROM=ColaCuentaProm
      - EXCHANGEPROMEDIO=ExchangePromedio
      - TOTALCUENTAPROM=$cant_cuenta_promedio
      - TOTALTRANSFORMADORES=$cant_transf
      - ID=$i" >> $archivo_salida
done 

for ((i=0; i<$cant_cuenta_promedio; i++)); do 
	definicion_base "cuenta_prom" $i "cuentaProm" 
	agregar_dependencias_comunes
        agregar_dependencia $CLASIFICADOR $cant_clasif
        agregar_dependencia $TRANSFORMADOR $cant_transf
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLACUENTAPROM=ColaCuentaProm
      - COLARESPUESTAS=Respuestas
      - EXCHANGECUENTAPROMEOF=ExchangeCuentaPromEof
      - ID=$i" >> $archivo_salida
done 

for ((i=0; i<$cant_sum_top; i++)); do
	definicion_base "sum_top" $i "sumTop" 
	agregar_dependencias_comunes
	agregar_dependencia $CLASIFICADOR $cant_clasif
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLASUMTOP=ColaSumTop
      - EXCHANGESUMTOPEOF=ExchangeSumTopEof
      - EXCHANGETOPPARCIAL=ExchangeTopParcial
      - TOTALTOPPARCIAL=$cant_agr_top" >> $archivo_salida
done

for ((i=0; i<$cant_agr_top; i++)); do
	definicion_base "agregador_top" $i "agregadorTop" 
	agregar_dependencias_comunes
	agregar_dependencia $CLASIFICADOR $cant_clasif
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLASUMTOP=ColaSumTop
      - COLARESPUESTAS=Respuestas
      - EXCHANGESUMTOPEOF=ExchangeSumTopEof
      - EXCHANGETOPPARCIAL=ExchangeTopParcial
      - EXCHANGETOPGLOBAL=ExchangeTopGlobal
      - TOTALTOPGLOBAL=$cant_join_top
      - TOTALSUMTOP=$cant_sum_top
      - ID=$i" >> $archivo_salida
done 

for ((i=0; i<$cant_join_top; i++)); do
	definicion_base "join_top" $i "joinTop"
	agregar_dependencias_comunes
	agregar_dependencia $CLASIFICADOR $cant_clasif
	echo "    environment:
      - PYTHONUNBUFFERED=1
      - MOMHOST=rabbitmq
      - COLARESPUESTAS=Respuestas
      - EXCHANGETOPGLOBAL=ExchangeTopGlobal
      - TOTALTOPPARCIAL=$cant_agr_top
      - ID=$i" >> $archivo_salida
done