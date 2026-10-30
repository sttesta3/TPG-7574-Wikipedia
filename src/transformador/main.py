import os
import re
import sys
import nltk
import signal
import threading
import traceback
from nltk.corpus import stopwords
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from clienteLock import ClienteLock

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
EXCHANGETRANSFORMADOREOF = os.environ["EXCHANGETRANSFORMADOREOF"]
TOTALPROMEDIO = int(os.environ["TOTALPROMEDIO"])
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])
TOTALCLASIFICADORES = int(os.environ["TOTALCLASIFICADORES"])

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'


class Transformador:
    def __init__(self):
        self.stopWords = set(stopwords.words('english')) | set(stopwords.words('french'))
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.exchangePromedio = []
        self.exchangeCuentaProm = []

        for i in range(TOTALPROMEDIO):
            self.exchangePromedio.append(MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + str(i)]))

        for i in range(TOTALCUENTAPROM):
            self.exchangeCuentaProm.append(MessageMiddlewareExchange(MOMHOST, EXCHANGECUENTAPROM, [EXCHANGECUENTAPROM + "_" + str(i)]))

        self.colaEOF = MessageMiddlewareExchange(MOMHOST, EXCHANGETRANSFORMADOREOF, [EXCHANGETRANSFORMADOREOF])
        self.colaEOFSend = MessageMiddlewareExchange(MOMHOST, EXCHANGETRANSFORMADOREOF, [EXCHANGETRANSFORMADOREOF])

        self.clientes = {}


    def _resumenAPalabras(self, resumen: str) -> dict[str]:
        palabrasSinStop = {}
        palabras = re.findall(WORD_REGEX, resumen.lower())
        for palabra in palabras:
            if palabra not in self.stopWords and not re.fullmatch(NUMBER_REGEX, palabra):
                palabrasSinStop[palabra] = 1
        return palabrasSinStop


    def _procesarData(self, mensaje: TransformadorMensajeSistema) -> None:
        if mensaje.clienteId not in self.clientes:
            self.clientes[mensaje.clienteId] = ClienteLock(TOTALCLASIFICADORES)
        
        self.clientes[mensaje.clienteId].nuevoMensaje()

        palabras = self._resumenAPalabras(mensaje.resumen)
        self.colaSumTop.send(PalabrasMensajeSistema(mensaje.clienteId, mensaje.url, mensaje.lenguaje, palabras).aBytes())
        if mensaje.fecha <= 2020:
            nodo = mensaje.clienteId.int % TOTALPROMEDIO
            self.exchangePromedio[nodo].send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())
        else:
            nodo = mensaje.clienteId.int % TOTALCUENTAPROM
            self.exchangeCuentaProm[nodo].send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())

        self.clientes[mensaje.clienteId].nuevaRespuesta()


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
            print(e)
            print(traceback.format_exc())
            nack()


    def _manejarEof(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)

            if self.clientes[mensaje.clienteId].llegadaEof():
                self.colaSumTop.send(mensaje.aBytes())

                nodo = mensaje.clienteId.int % TOTALPROMEDIO
                self.exchangePromedio[nodo].send(mensaje.aBytes())

                del self.clientes[mensaje.clienteId]
            ack()
        except Exception as e:
            print(e)
            nack()

    
    def _controlarEof(self):
        self.colaEOF.start_consuming(self._manejarEof)


    def iniciar(self):
        threading.Thread(target=self._controlarEof, daemon=True).start()
        self.colaTransformador.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        # Manejar el thread
        self.colaTransformador.close()
        self.colaSumTop.close()
        self.colaEOFSend.close()
        self.colaEOF.close()
        for i in range(TOTALCUENTAPROM):
            self.exchangeCuentaProm[i].close()
        for i in range(TOTALPROMEDIO):
            self.exchangePromedio[i].close()
        sys.exit(0)


def main() -> int:
    nltk.download('stopwords')
    transformador = Transformador()
    signal.signal(signal.SIGTERM, lambda signum, frame: transformador.manejarSigterm())
    transformador.iniciar()
    return 0


if __name__ == "__main__":
    main()