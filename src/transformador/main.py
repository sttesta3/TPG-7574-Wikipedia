import os
import re
import logging
import sys
import nltk
import signal
import threading
import traceback
from nltk.corpus import stopwords
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, TransformadorLoteMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema, PalabrasLoteMensajeSistema, CantidadPalabrasLoteMensajeSistema
from middleware import MessageMiddlewareQueue, MessageMiddlewareExchange
from contadorDistribuido import contadorDistribuido

MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
EXCHANGEPROMEDIO = os.environ["EXCHANGEPROMEDIO"]
EXCHANGETRANSFORMADOREOF = os.environ["EXCHANGETRANSFORMADOREOF"]
TOTALPROMEDIO = int(os.environ["TOTALPROMEDIO"])

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'


class Transformador:
    def __init__(self):
        self.stopWords = set(stopwords.words('english')) | set(stopwords.words('french'))
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR)
        self.colaSumTop = MessageMiddlewareQueue(MOMHOST, COLASUMTOP)
        self.colaCuentaProm = MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM)
        self.exchangePromedio = []

        for i in range(TOTALPROMEDIO):
            self.exchangePromedio.append(MessageMiddlewareExchange(MOMHOST, EXCHANGEPROMEDIO, [EXCHANGEPROMEDIO + "_" + str(i)]))

        self.contador = contadorDistribuido(MOMHOST, EXCHANGETRANSFORMADOREOF, self._finalizarCliente, self.colaTransformador.remote_execution)


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

        secuencia = mensajeLote.secuencia
        nodo = mensajeLote.clienteId.int % TOTALPROMEDIO
        self.colaCuentaProm.send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, cuentaPromedio, secuencia).aBytes())
        self.exchangePromedio[nodo].send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, promedio, secuencia).aBytes())
        self.colaSumTop.send(PalabrasLoteMensajeSistema(mensajeLote.clienteId, palabrasSumTop, secuencia).aBytes())


    def _finalizarCliente(self, clienteId, fin: FinMensajeSistema, originador: bool) -> None:
        nodo = clienteId.int % TOTALPROMEDIO
        self.exchangePromedio[nodo].send(FinMensajeSistema(clienteId, fin.totalMsg).aBytes())

        if originador:
            logging.info(f"Mando EOF de {clienteId} con total {fin.totalMsg}")
            self.colaSumTop.send(FinMensajeSistema(clienteId, fin.totalMsg).aBytes())


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self.contador.eofRecibido(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def iniciar(self):
        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)
        thread_contador.start()
        self.colaTransformador.start_consuming(self.procesarMensaje)
        thread_contador.join()
        self._close_connections()


    def _close_connections(self):
        self.colaTransformador.close()
        self.colaSumTop.close()
        self.colaCuentaProm.close()
        for i in range(TOTALPROMEDIO):
            self.exchangePromedio[i].close()
        self.contador.cerrar()


    def manejarSigterm(self) -> None:
        self.contador.detener()
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
