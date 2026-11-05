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


class Promedio:
    def __init__(self):
        self.clientes = {}
        self.exchangePromedio = MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + ID])
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM)

    def _procesarData(self, mensajes: CantidadPalabrasLoteMensajeSistema) -> None:
        clienteId = str(mensajes.clienteId)
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [0, 1, 0]

        for mensaje in mensajes.mensajes:
            self.clientes[clienteId][0] += mensaje.cantidad
            self.clientes[clienteId][1] += 1


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.clientes[str(mensaje.clienteId)][2] += 1

        if self.clientes[str(mensaje.clienteId)][2] == TOTALTRANSFORMADORES:
            promedio_float = self.clientes[str(mensaje.clienteId)][0] / self.clientes[str(mensaje.clienteId)][1]
            promedio = self.clientes[str(mensaje.clienteId)][0] // self.clientes[str(mensaje.clienteId)][1] 
            logging.info(f"Total: {self.clientes[str(mensaje.clienteId)][0]}")
            logging.info(f"Cuenta: {self.clientes[str(mensaje.clienteId)][1]}")
            logging.info(f"Promedio flotante: {promedio_float}")
            logging.info(f"Promedio : {promedio}") 
            
            self.colaCuentaProm.send(FinPromMensajeSistema(mensaje.clienteId, promedio).aBytes())

            del self.clientes[str(mensaje.clienteId)]
        
    
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
