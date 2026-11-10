import uuid
import logging
import threading
from middleware import MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, FinPromMensajeSistema, AnuncioMensajeSistema


class EstadoCliente():
    def __init__(self) -> None:
        self.total = None #cantidad total de mensajes, arranca en None hasta que sepamos cuanto es
        self.fin = None
        self.secuencias_anunciadas = set()
        self.finalizando = False

        self.secuencias_propias = set()
        self.anunciado = False
        self.originador_eof = False


class contadorDistribuido():
    def __init__(self, host: str, exchange: str, fnFinalizar, ejecutarEnPrincipal) -> None:
        self.fnFinalizar = fnFinalizar
        self.ejecutarEnPrincipal = ejecutarEnPrincipal

        self.lock = threading.Lock()
        self.secuencias = {}
        self.finalizados = set()

        self.consumidor = MessageMiddlewareExchange(host, exchange, [exchange])
        self.publicador = MessageMiddlewareExchange(host, exchange, [exchange])


    def _estado(self, clienteId: uuid.UUID) -> EstadoCliente:
        if clienteId not in self.secuencias:
            self.secuencias[clienteId] = EstadoCliente()
        return self.secuencias[clienteId]


    def yaFinalizado(self, clienteId: uuid.UUID) -> bool:
        with self.lock:
            return clienteId in self.finalizados


    def eofRecibido(self, mensaje: FinMensajeSistema | FinPromMensajeSistema) -> None:
        clienteId = mensaje.clienteId
        with self.lock:
            if clienteId in self.finalizados:
                return
            self._estado(clienteId).originador_eof = True
        logging.info(f"[contador] EOF de {clienteId} con total {mensaje.totalMsg}")
        self.publicador.send(mensaje.aBytes())


    def procesado(self, clienteId: uuid.UUID, secuencia: int) -> None:
        with self.lock:
            if clienteId in self.finalizados:
                return
            estado = self._estado(clienteId)
            if secuencia in estado.secuencias_propias:
                return
            estado.secuencias_propias.add(secuencia)
            anunciar = estado.anunciado
        if anunciar:
            self.publicador.send(AnuncioMensajeSistema(clienteId, [secuencia]).aBytes())


    def _anunciarPropias(self, clienteId: uuid.UUID) -> None:
        with self.lock:
            if clienteId in self.finalizados:
                return
            estado = self._estado(clienteId)
            estado.anunciado = True
            secuencias = list(estado.secuencias_propias)
        self.publicador.send(AnuncioMensajeSistema(clienteId, secuencias).aBytes())


    def _finalizar(self, clienteId: uuid.UUID) -> None:
        with self.lock:
            if clienteId in self.finalizados:
                return
            estado = self.secuencias.pop(clienteId)
            self.finalizados.add(clienteId)
        logging.info(f"[contador] Cliente {clienteId} finalizado: total={estado.total} originador={estado.originador_eof}")
        self.fnFinalizar(clienteId, estado.fin, estado.originador_eof)


    def _manejarControl(self, bytes, ack, nack) -> None:
        try:
            mensaje = recvMensajeSistema(bytes)
            clienteId = mensaje.clienteId
            finalizar = False

            with self.lock:
                if clienteId not in self.finalizados:
                    estado = self._estado(clienteId)

                    if isinstance(mensaje, (FinMensajeSistema, FinPromMensajeSistema)):
                        if estado.total is None:
                            estado.fin = mensaje
                            estado.total = mensaje.totalMsg
                            self.ejecutarEnPrincipal(lambda: self._anunciarPropias(clienteId))

                    elif isinstance(mensaje, AnuncioMensajeSistema):
                        estado.secuencias_anunciadas.update(mensaje.secuencias)

                    if (estado.total is not None and not estado.finalizando
                            and estado.secuencias_anunciadas >= set(range(1, estado.total + 1))):
                        estado.finalizando = True
                        finalizar = True

            if finalizar:
                self.ejecutarEnPrincipal(lambda: self._finalizar(clienteId))
            ack()
        except Exception as e:
            logging.error(f"[contador] Mensaje de control descartado: {e}")
            ack()


    def iniciar(self) -> None:
        self.consumidor.start_consuming(self._manejarControl)


    def detener(self) -> None:
        self.consumidor.remote_stop()


    def cerrar(self) -> None:
        self.consumidor.close()
        self.publicador.close()
