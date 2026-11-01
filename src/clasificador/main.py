import os
import sys
import logging
import signal
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue,MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema
from protocolo.mensajesCliente import LENGUAJEINGLES, LENGUAJEFRANCES

MOMHOST = os.environ["MOMHOST"]
COLADATOS = os.environ["COLADATOS"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLAIMGDESCARGA = os.environ["COLAIMGDESCARGA"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
CLASIFICADOREXCHANGEEOF = os.environ["CLASIFICADOREXCHANGEEOF"]

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)

        self.colaEOF = MessageMiddlewareExchange(MOMHOST, CLASIFICADOREXCHANGEEOF, [CLASIFICADOREXCHANGEEOF])
        self.colaEOFSend = MessageMiddlewareExchange(MOMHOST, CLASIFICADOREXCHANGEEOF, [CLASIFICADOREXCHANGEEOF])

        self.clientes = {}


    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        if loteMensaje.clienteId not in self.clientes:
            self.clientes[loteMensaje.clienteId] = ClienteLock()

        self.clientes[loteMensaje.clienteId].nuevoMensaje()
         
        for mensaje in loteMensaje.lote:
            if mensaje.lenguaje == LENGUAJEINGLES and mensaje.fecha <= 2020:
                self.colaRespuestas.send(Respuesta1MensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha).aBytes())
            if mensaje.fecha <= 2020 and mensaje.biografia == 1:
                self.colaImgDescarga.send(ImgMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.nombre, mensaje.imgUrl).aBytes())
            self.colaTransformador.send(TransformadorMensajeSistema(loteMensaje.clienteId, mensaje.url, mensaje.fecha, mensaje.resumen, mensaje.lenguaje).aBytes())

        self.clientes[loteMensaje.clienteId].nuevaRespuesta()
            

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaEOFSend.send(mensaje.aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
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

            if self.clientes[mensaje.clienteId].llegadaEof():
                self.colaImgDescarga.send(mensaje.aBytes())
                self.colaTransformador.send(mensaje.aBytes())
                
                del self.clientes[mensaje.clienteId]

            ack()
        except Exception as e:
            logging.info(e)
            nack()

    
    def _controlarEof(self):
        self.colaEOF.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaDatos.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        # TODO: aca faltaria ver que hacer con el thread q queda dando vueltas
        self.colaDatos.close()
        self.colaRespuestas.close()
        self.colaImgDescarga.close()
        self.colaTransformador.close()
        self.colaEOFSend.close()
        self.colaEOF.close()
        sys.exit(0)


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()
