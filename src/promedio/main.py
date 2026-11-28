import os
import signal
import logging
import traceback
import threading
from wal import Wal
from latido import Latido
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, CantidadPalabrasLoteMensajeSistema, FinPromMensajeSistema, ClienteMuertoMensajeSistema


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

        self.wal = Wal()


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
            logging.debug(f"Total: {estado[SUMA]}")
            logging.debug(f"Cuenta: {estado[CUENTA]}")
            logging.debug(f"Promedio flotante: {promedio_float}")
            logging.debug(f"Promedio : {promedio}")

            # Todos los cuentaProm necesitan el promedio para filtrar sus articulos
            for cola in self.colaCuentaProm:
                cola.send(FinPromMensajeSistema(mensaje.clienteId, promedio, mensaje.totalMsg).aBytes())

            self.contador.finalizar(mensaje.clienteId)
            del self.clientes[clienteId]
        
    
    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self.wal.guardarMensaje(bytes)
            
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId) or self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}")            
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                del self.clientes[mensaje.clienteId]
                self.colaCuentaProm.send(bytes)
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def _recuperarse(self):
        try:
            self.clientes, contador = self.wal.recuperarEstado()
            self.contador.load_state(contador)

            for logBytes in self.wal.recuperarMensajes():
                log = recvMensajeSistema(logBytes)

                if isinstance(log, FinMensajeSistema):
                    if self.contador.eofRecibido(log.clienteId, log.origen):
                        self._finalizarCliente(log.clienteId)
                        self.contador.finalizar(log.clienteId)
                elif self.contador.yaFinalizado(log.clienteId) or self.contador.yaProcesado(log.clienteId, log.secuencia):
                    logging.debug(f"Descarto lote {log.secuencia} de {log.clienteId}")
                else:
                    self.contador.procesado(log.clienteId, log.secuencia)
                    self._procesarData(log)
        except Exception as e:
            print(f"{e}")
            print(traceback.format_exc())


    def iniciar(self):
        latido = Latido(self.colaPromedio.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()
        
        self._recuperarse()

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
