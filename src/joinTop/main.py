import os
import signal
import logging
import traceback
import threading
from wal import Wal
from latido import Latido
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, Respuesta4MensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
EXCHANGETOPGLOBAL = os.environ["EXCHANGETOPGLOBAL"]
TOTALTOPPARCIAL = int(os.environ["TOTALTOPPARCIAL"])
ID = os.environ["ID"]


class JoinTop:
    def __init__(self):
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.exchangeTopGlobal = MessageMiddlewareExchange(MOMHOST, EXCHANGETOPGLOBAL, [EXCHANGETOPGLOBAL+"_"+ID])

        self.clientes = {}
        self.wal = Wal()


    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [0, {}]

        for mensaje in mensajes.mensajes:
            logging.debug(f"[join] Recibi {clienteId} top parcial {mensaje.palabras}")
            self.clientes[clienteId][1] = self.clientes[clienteId][1] | mensaje.palabras

    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:20])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        logging.debug(f"[join] Recibi {mensaje.clienteId} EOF")
        self.clientes[mensaje.clienteId][0] += 1

        if self.clientes[mensaje.clienteId][0] == TOTALTOPPARCIAL:
            self.colaRespuestas.send(Respuesta4MensajeSistema(mensaje.clienteId, self._top20(self.clientes[mensaje.clienteId][1])).aBytes())
            self.colaRespuestas.send(mensaje.aBytes())
            self.wal.borrarLog(mensaje.clienteId)
            del self.clientes[mensaje.clienteId]


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self.wal.guardarMensaje(bytes)
            ack()
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def _recuperarLog(self):
        for log in self.wal.recuperarLogs():
            if isinstance(log, FinMensajeSistema):
                self._procesarEOF(log)
            else:
                self._procesarData(log)


    def iniciar(self):
        latido = Latido(self.colaDatos.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self._recuperarLog()
        self.exchangeTopGlobal.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.exchangeTopGlobal.remote_stop()


    def _close_connections(self):
        self.colaRespuestas.close()
        self.exchangeTopGlobal.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    joinTop = JoinTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: joinTop.manejarSigterm())
    joinTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
