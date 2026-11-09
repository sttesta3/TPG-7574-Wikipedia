import os
import re
import logging
import sys
import nltk
import signal
import threading
import traceback
from nltk.corpus import stopwords
from protocolo.mensajesSistema import CantidadMensajes, recvMensajeSistema, FinMensajeSistema, TransformadorLoteMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema, PalabrasLoteMensajeSistema, CantidadPalabrasLoteMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from clienteLock import ClienteLock

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
EXCHANGETRANSFORMADOREOF = os.environ["EXCHANGETRANSFORMADOREOF"]
TOTALPROMEDIO = int(os.environ["TOTALPROMEDIO"])
TOTALCLASIFICADORES = int(os.environ["TOTALCLASIFICADORES"])
COLASINCRONIZADOR = os.environ["COLASINCRONIZADOR"]

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'


class Transformador:
    def __init__(self):
        self.stopWords = set(stopwords.words('english')) | set(stopwords.words('french'))
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM)
        self.exchangePromedio = []

        self.colaSincronizador = MessageMiddlewareQueue(MOMHOST, COLASINCRONIZADOR)
        self.exchangeSincronizacion = MessageMiddlewareExchange(MOMHOST, EXCHANGETRANSFORMADOREOF, [EXCHANGETRANSFORMADOREOF])

        for i in range(TOTALPROMEDIO):
            self.exchangePromedio.append(MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + str(i)]))

        self.clientes = {}


    def _resumenAPalabras(self, resumen: str) -> dict[str]:
        palabrasSinStop = {}
        palabras = re.findall(WORD_REGEX, resumen.lower())
        for palabra in palabras:
            if palabra not in self.stopWords and not re.fullmatch(NUMBER_REGEX, palabra):
                palabrasSinStop[palabra] = 1
        
        # Filtro contra abstracts vacios (si el abstract es una unica palabra y es 'nan', entonces es vacio)
        if len(palabrasSinStop) == 1 and 'nan' in palabrasSinStop:
            return {}
        else:
            return palabrasSinStop


    def _procesarData(self, mensajeLote: TransformadorLoteMensajeSistema) -> None:
        if mensajeLote.clienteId not in self.clientes:
            self.clientes[mensajeLote.clienteId] = ClienteLock(TOTALCLASIFICADORES)

        palabrasSumTop = []
        cuentaPromedio = []
        promedio = []

        for mensaje in mensajeLote.mensajes:
            palabras = self._resumenAPalabras(mensaje.resumen)

            if len(palabras) > 0: 
                palabrasSumTop.append(PalabrasMensajeSistema( mensaje.url, mensaje.lenguaje, palabras))
                if mensaje.fecha <= 2020:                            
                    promedio.append(CantidadPalabraMensajeSistema( mensaje.url, len(palabras)))
                else:
                    cuentaPromedio.append(CantidadPalabraMensajeSistema( mensaje.url, len(palabras)))

        nodo = mensajeLote.clienteId.int % TOTALPROMEDIO
        self.colaCuentaProm.send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, cuentaPromedio).aBytes())
        self.exchangePromedio[nodo].send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, promedio).aBytes())
        self.colaSumTop.send(PalabrasLoteMensajeSistema(mensajeLote.clienteId, palabrasSumTop).aBytes())

        self.clientes[mensajeLote.clienteId].nuevoMensaje()

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaEOFSend.send(mensaje.aBytes())

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
        thread_eof = threading.Thread(target=self._mainControl, daemon=True)
        thread_eof.start()
        self.colaTransformador.start_consuming(self.procesarMensaje)
        thread_eof.join()
        self._close_connections()


    def _close_connections(self):
        self.colaTransformador.close()
        self.colaSumTop.close()
        self.colaEOFSend.close()
        self.colaEOF.close()
        self.colaCuentaProm.close()
        for i in range(TOTALPROMEDIO):
            self.exchangePromedio[i].close()


    def manejarSigterm(self) -> None:
        self.colaEOF.remote_stop()
        self.colaTransformador.remote_stop()
        

def main() -> int:
    logging.basicConfig(level=logging.INFO)
    nltk.download('stopwords')
    transformador = Transformador()
    signal.signal(signal.SIGTERM, lambda signum, frame: transformador.manejarSigterm())
    transformador.iniciar()
    return 0


if __name__ == "__main__":
    main()
