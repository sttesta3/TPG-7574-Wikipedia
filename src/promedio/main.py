import os
import sys
import logging
import signal
import traceback
from middleware import MessageMiddlewareQueue
from contadorEof import contadorEof
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, CantidadPalabrasLoteMensajeSistema, FinPromMensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLAPROMEDIO = os.environ["COLAPROMEDIO"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])
TOTALTRANSFORMADORES = int(os.environ["TOTALTRANSFORMADORES"])
ID = os.environ["ID"]

SUMA = 0
CUENTA = 1
CUENTA_INICIAL = 0


class Promedio:
    def __init__(self):
        self.clientes = {}
        self.contador = contadorEof(TOTALTRANSFORMADORES)
        self.colaPromedio = MessageMiddlewareQueue(MOMHOST, COLAPROMEDIO + "_" + ID)
        self.colaCuentaProm = [MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM + "_" + str(i)) for i in range(TOTALCUENTAPROM)]

    def _estado(self, clienteId: str) -> list:
        if clienteId not in self.clientes:
            self.clientes[clienteId] = [0, CUENTA_INICIAL]
        return self.clientes[clienteId]

    def _procesarData(self, mensajes: CantidadPalabrasLoteMensajeSistema) -> None:
        estado = self._estado(str(mensajes.clienteId))

        for mensaje in mensajes.mensajes:
            estado[SUMA] += mensaje.cantidad
            estado[CUENTA] += 1


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        clienteId = str(mensaje.clienteId)
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            estado = self._estado(clienteId)
            promedio_float = estado[SUMA] / estado[CUENTA]
            promedio = estado[SUMA] // estado[CUENTA]
            logging.info(f"Total: {estado[SUMA]}")
            logging.info(f"Cuenta: {estado[CUENTA]}")
            logging.info(f"Promedio flotante: {promedio_float}")
            logging.info(f"Promedio : {promedio}")

            # Todos los cuentaProm necesitan el promedio para filtrar sus articulos
            for cola in self.colaCuentaProm:
                cola.send(FinPromMensajeSistema(mensaje.clienteId, promedio, mensaje.totalMsg).aBytes())

            self.clientes.pop(clienteId, None)
            self.contador.finalizar(mensaje.clienteId)
        
    
    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def iniciar(self):
        self.colaPromedio.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaPromedio.remote_stop()


    def _close_connections(self):
        self.colaPromedio.close()
        for cola in self.colaCuentaProm:
            cola.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    promedio = Promedio()
    signal.signal(signal.SIGTERM, lambda signum, frame: promedio.manejarSigterm())
    promedio.iniciar()
    return 0


if __name__ == "__main__":
    main()
