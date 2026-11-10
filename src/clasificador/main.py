import os
import sys
import logging
import signal
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue,MessageMiddlewareExchange
from protocolo.mensajesSistema import EOF_CLASIFICADOR_IMG, EOF_CLASIFICADOR_TRANS, FinMensajeSincronizacion, recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema, TransformadorLoteMensajeSistema, CantidadMensajes
from protocolo.mensajesCliente import LENGUAJEINGLES, LENGUAJEFRANCES
from worker.worker import WorkerSincronizado

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
CLASIFICADOREXCHANGEEOF = os.environ["CLASIFICADOREXCHANGEEOF"]
COLASINCRONIZADOR = os.environ["COLASINCRONIZADOR"]

MENSAJES_RECIBIDOS = 0
MENSAJES_IMG_ENVIADOS = 1
MENSAJES_RTA1_ENVIADOS = 2

class Clasificador(WorkerSincronizado):
    def __init__(self):
        super().__init__(cola_datos=COLADATOS,exchange=CLASIFICADOREXCHANGEEOF)

        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)

        self.clientes = {}

    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        if loteMensaje.clienteId not in self.clientes:
            self.clientes[loteMensaje.clienteId] = [ ClienteLock(), 0, 0 ]

        logging.info(f"Recibo mensaje de {loteMensaje.clienteId}")            
        transformadorMensajes = []
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
                self.clientes[loteMensaje.clienteId][MENSAJES_RTA1_ENVIADOS] += 1            
            if mensaje.fecha <= 2020 and mensaje.biografia == 1:
                self.colaImgDescarga.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl).aBytes())
                self.clientes[loteMensaje.clienteId][MENSAJES_IMG_ENVIADOS] += 1            
                
            transformadorMensajes.append(TransformadorMensajeSistema(mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje))
        self.clientes[loteMensaje.clienteId][MENSAJES_RECIBIDOS].nuevoMensaje()            

        self.colaTransformador.send(TransformadorLoteMensajeSistema(loteMensaje.clienteId, transformadorMensajes).aBytes())

    def _finProcesamiento(self, mensaje):
        clienteId = mensaje.clienteId
        totalMsg=self.clientes[clienteId][MENSAJES_IMG_ENVIADOS]
        self.colaSincronizador.send(FinMensajeSincronizacion(clienteId, totalMsg=totalMsg, tipoMensaje=EOF_CLASIFICADOR_IMG).aBytes())
        totalMsg=self.clientes[clienteId][MENSAJES_RECIBIDOS].cantMensajes()
        self.colaSincronizador.send(FinMensajeSincronizacion(clienteId, totalMsg=totalMsg, tipoMensaje=EOF_CLASIFICADOR_TRANS).aBytes())

        # TODO: EOF para RTA 1 ?                 
        del self.clientes[mensaje.clienteId]

    def _get_mensajes_recibidos(self, clienteId) -> int:
        return self.clientes[clienteId][MENSAJES_RECIBIDOS].cantMensajes()

    def manejarSigterm(self) -> None:
        super().manejarSigterm()

    def _close_connections(self):
        super()._close_connections()
        self.colaRespuestas.close()
        self.colaImgDescarga.close()
        self.colaTransformador.close()

def main() -> int:
    logging.basicConfig(level=logging.INFO)
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()
