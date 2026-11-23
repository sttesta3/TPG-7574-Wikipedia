import os
import sys
import logging
import signal
import traceback
from middleware import MessageMiddlewareQueue
from contadorEof import contadorEof
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, Respuesta4MensajeSistema, ETAPA_JOIN, origenGateway


MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLATOPGLOBAL = os.environ["COLATOPGLOBAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
ID = os.environ["ID"]


class JoinTop:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaTopGlobal = MessageMiddlewareQueue(MOMHOST, COLATOPGLOBAL + "_" + ID)

        self.clientes = {}
        self.contador = contadorEof(TOTALTOPPARCIAL)


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = {}

        for mensaje in mensajes.mensajes:
            logging.info(f"[join] Recibi {clienteId} top parcial {mensaje.palabras}")
            self.clientes[clienteId] = self.clientes[clienteId] | mensaje.palabras

    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        logging.info(f"[join] Recibi {mensaje.clienteId} EOF de {mensaje.origen}")
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            palabras = self.clientes.pop(mensaje.clienteId, {})
            idRespuesta = (ETAPA_JOIN, int(ID), 0, 0)
            self.colaRespuestas.send(Respuesta4MensajeSistema(mensaje.clienteId, self._top20(palabras), idRespuesta).aBytes())
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId, origen=origenGateway(ETAPA_JOIN, int(ID))).aBytes())
            self.contador.finalizar(mensaje.clienteId)


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto parcial de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto parcial {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def iniciar(self):
        self.colaTopGlobal.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaTopGlobal.remote_stop()


    def _close_connections(self):
        self.colaRespuestas.close()
        self.colaTopGlobal.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    joinTop = JoinTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: joinTop.manejarSigterm())
    joinTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
