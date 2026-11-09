# TPG-7574-Wikipedia

## Sincronizacion de eofs 

### Modelo de sincronizacion elegido 

Barrera 

### Secuencia de pasos 

1. La etapa previa envia EOF CantidadMensajesEnviados a la colaSincronizador
2. Los nodos de sincronizacion envian un mensaje CantidadMensajes a exchangeSincronizacion
3. Los nodos de la etapa actual responden enviando a colaSincronizador su cantidad de mensajes recibidos y procesados exitosamente
4. Cuando los nodos de sincronizacion reunen todas las respuestas, revisan si coinciden las cantidades y de coincidir envian EOF a los nodos de la etapa actual. Caso contrario, los nodos de sincronizacion consultaran mas tarde (probablemente backoff exponencial, o esperas constantes de X segundos) 
5. Los nodos de la etapa actual envian EOF CantidadMensajesEnviados (se dispara nuevamente el proceso para la etapa siguiente) 

## Ejecuccion

- make build: Crear un archivo docker compose custom (te pregunta los parametros)

- make switch: Elegir un archivo yaml para ejecutar (sobreescribe docker-compose.yaml con dicho archivo)

- make up: Ejecuta docker compose con docker-compose.yaml 

- make down: Detener y eliminar nodos 
