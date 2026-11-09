import os
import sys
import logging
import signal
import threading
from clienteLock import ClienteLock
from middleware import MessageMiddlewareQueue,MessageMiddlewareExchange
from protocolo.mensajesSistema import EOF_CLASIFICADOR_IMG, EOF_CLASIFICADOR_TRANS, FinMensajeSincronizacion, recvMensajeSistema, FinMensajeSistema, LoteDataMensajeSistema, ImgMensajeSistema, Respuesta1MensajeSistema, TransformadorMensajeSistema, TransformadorLoteMensajeSistema, CantidadMensajes
from protocolo.mensajesCliente import LENGUAJEINGLES, LENGUAJEFRANCES

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

class Clasificador:
    def __init__(self):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, COLADATOS)
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
        self.colaImgDescarga = MessageMiddlewareQueue(MOMHOST, COLAIMGDESCARGA)
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)

        self.colaSincronizador = MessageMiddlewareQueue(MOMHOST, COLASINCRONIZADOR)
        self.exchangeSincronizacion = MessageMiddlewareExchange(MOMHOST, CLASIFICADOREXCHANGEEOF, [CLASIFICADOREXCHANGEEOF])

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

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            nack()

    def _manejarMensajeControl(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, CantidadMensajes):
                mensaje.setCantidad(cant=self.clientes[mensaje.clienteId][MENSAJES_RECIBIDOS].cantMensajes())
                self.colaSincronizador.send(mensaje.aBytes())
            else: 
                clienteId = mensaje.clienteId
                totalMsg=self.clientes[clienteId][MENSAJES_IMG_ENVIADOS]
                self.colaSincronizador.send(FinMensajeSincronizacion(clienteId, totalMsg=totalMsg, tipoMensaje=EOF_CLASIFICADOR_IMG).aBytes())
                totalMsg=self.clientes[clienteId][MENSAJES_RECIBIDOS].cantMensajes()
                self.colaSincronizador.send(FinMensajeSincronizacion(clienteId, totalMsg=totalMsg, tipoMensaje=EOF_CLASIFICADOR_TRANS).aBytes())

                # TODO: EOF para RTA 1 ?                 
                del self.clientes[mensaje.clienteId]

            ack()
        except Exception as e:
            logging.info(e)
            nack()
    
    def _mainControl(self):
        self.exchangeSincronizacion.start_consuming(self._manejarMensajeControl)

    def iniciar(self):
        thread_sincronizacion = threading.Thread(target=self._mainControl, daemon=True)
        thread_sincronizacion.start()
        self.colaDatos.start_consuming(self.procesarMensaje)
        thread_sincronizacion.join()
        self._close_connections()

    def manejarSigterm(self) -> None:
        self.exchangeSincronizacion.remote_stop()
        self.colaDatos.remote_stop() #mando la señal para que el hilo que maneja corte el channel esto vuelve a lo
                                     #que va despues de invocar al hilo en iniciar

    def _close_connections(self):
        self.colaDatos.close()
        self.colaRespuestas.close()
        self.colaImgDescarga.close()
        self.colaTransformador.close()
        self.colaSincronizador.close()
        self.exchangeSincronizacion.close()

def main() -> int:
    logging.basicConfig(level=logging.INFO)
    clasificador = Clasificador()
    signal.signal(signal.SIGTERM, lambda signum, frame: clasificador.manejarSigterm())
    clasificador.iniciar()
    return 0


if __name__ == "__main__":
    main()
