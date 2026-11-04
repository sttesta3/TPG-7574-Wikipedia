import os
import sys
import signal
import logging
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinPromMensajeSistema, CantidadPalabraMensajeSistema, Respuesta5MensajeSistema, FinMensajeSistema

MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
ID = os.environ["ID"]
LOTE = 50


class CuentaProm:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeProm = MessageMiddlewareQueue(MOMHOST, EXCHANGECUENTAPROM)
        self.exchangeEof = MessageMiddlewareExchange(MOMHOST, "EOFS", ["EOFAS"])
        self.exchangeSendEof = MessageMiddlewareExchange(MOMHOST, "EOFS", ["EOFAS"])

        self.cliente = {}

    def _procesarData(self, mensaje: CantidadPalabraMensajeSistema) -> None:
        clientId = str(mensaje.clienteId)

        if clientId not in self.cliente:
            self.cliente[clientId] = ClienteLock()

        self.cliente[clientId].nuevoMensaje()

        with open(clientId, "a", encoding="utf-8") as f:
            f.write(f"{mensaje.url};;;;;{mensaje.cantidad}\n")

        self.cliente[clientId].nuevaRespuesta()


    def _procesarEOF(self, mensaje: FinPromMensajeSistema) -> None:
       self.exchangeSendEof.send(mensaje.aBytes())
        

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinPromMensajeSistema): # TODO: esta bien esto?
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            nack()

    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)

            if self.clientes[str(mensaje.clienteId)].llegadaEof():
                with open(str(mensaje.clienteId), "r", encoding="utf-8") as f:
                    data = {}
                    for linea in f.readlines():
                        url, cantidad = linea.strip().split(";;;;;", 1)
                        if int(cantidad) > mensaje.promedio:
                            data[url] = int(cantidad)
                            if len(data) == LOTE:
                                self.colaRespuestas.send(Respuesta5MensajeSistema(mensaje.clienteId,data).aBytes())
                                data = {}
                    if len(data) > 0:
                        self.colaRespuestas.send(Respuesta5MensajeSistema(mensaje.clienteId, data).aBytes())
                self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId).aBytes())
                
                os.remove(str(mensaje.clienteId))
                del self.clientes[str(mensaje.clienteId)]

            ack()
        except Exception as e:
            logging.info(e)
            nack()

    
    def _controlarEof(self):
        self.exchangeEof.start_consuming(self._manejarEof)


    def iniciar(self):
        thread_eof = threading.Thread(target=self._controlarEof, daemon=True)
        self.exchangeProm.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.exchangeProm.remote_stop()


    def _close_connections(self):
        self.exchangeProm.close()
        self.colaRespuestas.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    cuentaProm = CuentaProm()
    signal.signal(signal.SIGTERM, lambda signum, frame: cuentaProm.manejarSigterm())
    cuentaProm.iniciar()
    return 0


if __name__ == "__main__":
    main()
