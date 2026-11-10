import os
import sys
import logging
import signal
import traceback
from middleware import MessageMiddlewareExchange, MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, CantidadPalabrasLoteMensajeSistema, FinPromMensajeSistema


MOMHOST = os.environ["MOMHOST"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])
ID = os.environ["ID"]

SUMA = 0
CUENTA = 1
EOFS_RECIBIDOS = 2
CUENTA_INICIAL = 0


class Promedio:
    def __init__(self):
        self.clientes = {}
        self.exchangePromedio = MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + ID])
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM)

    def _estado(self, clienteId: str) -> list:
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [0, CUENTA_INICIAL, 0]
        return self.clientes[clienteId]

    def _procesarData(self, mensajes: CantidadPalabrasLoteMensajeSistema) -> None:
        estado = self._estado(str(mensajes.clienteId))

        for mensaje in mensajes.mensajes:
            estado[SUMA] += mensaje.cantidad
            estado[CUENTA] += 1


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        clienteId = str(mensaje.clienteId)
        estado = self._estado(clienteId)

        estado[EOFS_RECIBIDOS] += 1

        if estado[EOFS_RECIBIDOS] == TOTALTRANSFORMADORES:
            promedio_float = estado[SUMA] / estado[CUENTA]
            promedio = estado[SUMA] // estado[CUENTA]
            logging.info(f"Total: {estado[SUMA]}")
            logging.info(f"Cuenta: {estado[CUENTA]}")
            logging.info(f"Promedio flotante: {promedio_float}")
            logging.info(f"Promedio : {promedio}")

            self.colaCuentaProm.send(FinPromMensajeSistema(mensaje.clienteId, promedio, mensaje.totalMsg).aBytes())

            del self.clientes[clienteId]
        
    
    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            else:
                self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def iniciar(self):
        self.exchangePromedio.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.exchangePromedio.remote_stop()


    def _close_connections(self):
        self.exchangePromedio.close()
        self.colaCuentaProm.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    promedio = Promedio()
    signal.signal(signal.SIGTERM, lambda signum, frame: promedio.manejarSigterm())
    promedio.iniciar()
    return 0


if __name__ == "__main__":
    main()
