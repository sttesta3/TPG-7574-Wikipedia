from abc import ABC, abstractmethod
import os
import logging
import threading
from middleware import MessageMiddlewareQueue
from middleware.middleware import MessageMiddlewareExchange
from protocolo.mensajesSistema import recvMensajeSistema, LoteDataMensajeSistema, CantidadMensajes

MOMHOST = os.environ["MOMHOST"]
COLASINCRONIZADOR = os.environ["COLASINCRONIZADOR"]

MENSAJES_RECIBIDOS = 0
MENSAJES_IMG_ENVIADOS = 1
MENSAJES_RTA1_ENVIADOS = 2

class WorkerSincronizado(ABC):
    def __init__(self, exchange: str):
        self.colaSincronizador = MessageMiddlewareQueue(MOMHOST, COLASINCRONIZADOR)
        self.exchageSincronizacion = MessageMiddlewareExchange(MOMHOST,exchange,[exchange])
        self.clientes = {}

    @abstractmethod
    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        pass

    @abstractmethod
    def _finProcesamiento(self) -> None:
        pass

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
                self._finProcesamiento(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            nack()
    
    def _mainControl(self):
        self.exchangeSincronizacion.start_consuming(self._manejarMensajeControl)

    @abstractmethod
    def _start_consuming(self):
        pass

    def iniciar(self):
        thread_sincronizacion = threading.Thread(target=self._mainControl, daemon=True)
        thread_sincronizacion.start()
        self._start_consuming()        
        thread_sincronizacion.join()
        self._close_connections()

    @abstractmethod
    def _close_connections(self):
        pass
