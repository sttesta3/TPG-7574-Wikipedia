import os
import re
import sys
import nltk
import signal
from nltk.corpus import stopwords
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
EXCHANGECUENTAPROM = os.environ["EXCHANGECUENTAPROM"]
TOTALPROMEDIO = int(os.environ["TOTALPROMEDIO"])
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])

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

    def _resumenAPalabras(self, resumen: str) -> dict[str]:
        palabrasSinStop = {}
        palabras = re.findall(WORD_REGEX, resumen.lower())
        for palabra in palabras:
            if palabra not in self.stopWords and not re.fullmatch(NUMBER_REGEX, palabra):
                palabrasSinStop[palabra] = 1
        return palabrasSinStop


    def _procesarData(self, mensaje: TransformadorMensajeSistema) -> None:

        palabras = self._resumenAPalabras(mensaje.resumen)
        self.colaSumTop.send(PalabrasMensajeSistema(mensaje.clienteId, mensaje.url, mensaje.lenguaje, palabras).aBytes())
        if mensaje.fecha <= 2020:
            nodo = mensaje.clienteId.int % TOTALPROMEDIO
            self.exchangePromedio[nodo].send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())
        else:
            nodo = mensaje.clienteId.int % TOTALCUENTAPROM
            self.exchangeCuentaProm[nodo].send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaSumTop.send(mensaje.aBytes())
        
        nodo = mensaje.clienteId.int % TOTALPROMEDIO
        self.exchangePromedio[nodo].send(mensaje.aBytes())
        

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
            nack()


    def iniciar(self):
        self.colaTransformador.start_consuming(self.procesarMensaje)


    def manejarSigterm(self) -> None:
        self.colaTransformador.close()
        self.colaSumTop.close()
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