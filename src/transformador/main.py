import os
import re
import nltk
from nltk.corpus import stopwords
from mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLAPROMMENOR = os.environ["COLAPROMMENOR"]
EXCHANGEPROMMAYOR = os.environ["EXCHANGEPROMMAYOR"]
TOTALPROMMAYOR = int(os.environ["TOTALPROMMAYOR"])

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'

class Transformador:
    def __init__(self):
        self.stopWords = set(stopwords.words('english')) | set(stopwords.words('french'))
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.colaPromMenor = MessageMiddlewareQueue(MOMHOST, COLAPROMMENOR)
        self.exchangeProm = []

        for i in range(TOTALPROMMAYOR):
            self.exchangeProm.append(MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMMAYOR, [EXCHANGEPROMMAYOR + "_" + str(i)]))

    def _resumenAPalabras(self, resumen: str) -> dict[str]:
        palabrasSinStop = {}
        palabras = re.findall(WORD_REGEX, resumen.lower())
        for palabra in palabras:
            if palabra not in self.stopWords and not re.fullmatch(NUMBER_REGEX, palabra):
                palabrasSinStop[palabra] = 1
        print(palabrasSinStop.keys())
        return palabrasSinStop


    def _procesarData(self, mensaje: TransformadorMensajeSistema) -> None:

        palabras = self._resumenAPalabras(mensaje.resumen)
        self.colaSumTop.send(PalabrasMensajeSistema(mensaje.clienteId, mensaje.url, mensaje.lenguaje, palabras).aBytes())
        if mensaje.fecha <= 2020:
            self.colaPromMenor.send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())
        else:
            nodo = mensaje.clienteId.int % TOTALPROMMAYOR
            self.exchangeProm[nodo].send(CantidadPalabraMensajeSistema(mensaje.clienteId, mensaje.url, len(palabras)).aBytes())


    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        self.colaSumTop.send(mensaje.aBytes())
        #Enviar eof a los nodos de promedio


    def procesarMensaje(self, bytes, ack, nack):
        mensaje = recvMensajeSistema(bytes)
        if isinstance(mensaje, FinMensajeSistema): # TODO: esta bien esto?
            self._procesarEOF(mensaje)
        else:
            self._procesarData(mensaje)
        ack()

    def iniciar(self):
        self.colaTransformador.start_consuming(self.procesarMensaje)

def main() -> int:
    nltk.download('stopwords')
    transformador = Transformador()
    transformador.iniciar()
    return 0


if __name__ == "__main__":
    main()