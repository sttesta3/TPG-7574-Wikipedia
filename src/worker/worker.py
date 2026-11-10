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
    def __init__(self, cola_datos: str, exchange: str):
        self.colaDatos = MessageMiddlewareQueue(MOMHOST, cola_datos)
        self.colaSincronizador = MessageMiddlewareQueue(MOMHOST, COLASINCRONIZADOR)
        self.exchageSincronizacion = MessageMiddlewareExchange(MOMHOST,exchange,[exchange])
        self.clientes = {}

    @abstractmethod
    def _procesarData(self, loteMensaje: LoteDataMensajeSistema) -> None:
        pass

    @abstractmethod
    def _finProcesamiento(self, mensaje) -> None:
        pass

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            self._procesarData(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            nack()
    
    @abstractmethod
    def _get_mensajes_enviados(self, clienteId):
        pass

    def _manejarMensajeControl(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, CantidadMensajes):
                mensaje.setCantidad(cant=self._get_mensajes_enviados())
                self.colaSincronizador.send(mensaje.aBytes())
            else: 
                self._finProcesamiento(mensaje)
            ack()
        except Exception as e:
            logging.info(e)
            nack()
    
    def _mainControl(self):
        self.exchangeSincronizacion.start_consuming(self._manejarMensajeControl)

    def iniciar(self):
        thread_sincronizacion = threading.Thread(target=self._mainControl, daemon=True)
        thread_sincronizacion.start()
        self.colaDatos._start_consuming(self.procesarMensaje())        
        thread_sincronizacion.join()
        self._close_connections()

    @abstractmethod
    def _get_mensajes_recibidos(self, clienteId) -> int:
        pass

    def manejarSigterm(self) -> None:
        #mando la señal para que el hilo que maneja corte el channel esto vuelve a lo
        #que va despues de invocar al hilo en iniciar

        self.colaDatos.remote_stop()
        self.exchageSincronizacion.remote_stop()
        self.colaSincronizador.remote_stop()
        self.colaDatos.remote_stop() 

    def _close_connections(self):
        self.colaDatos.close()
        self.exchageSincronizacion.close()
        self.colaSincronizador.close()