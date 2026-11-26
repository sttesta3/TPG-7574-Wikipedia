import os
import re
import nltk
import signal
import logging
import threading
import traceback
from latido import Latido
from nltk.corpus import stopwords
from contadorEof import contadorEof
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema,ClienteMuertoMensajeSistema, TransformadorLoteMensajeSistema, PalabrasMensajeSistema, CantidadPalabraMensajeSistema, PalabrasLoteMensajeSistema, CantidadPalabrasLoteMensajeSistema


MOMHOST = os.environ["MOMHOST"]
COLATRANSFORMADOR = os.environ["COLATRANSFORMADOR"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLACUENTAPROM = os.environ["COLACUENTAPROM"]
COLAPROMEDIO = os.environ["COLAPROMEDIO"]
TOTALCLASIFICADORES = int(os.environ["TOTALCLASIFICADORES"])
ID = int(os.environ["ID"])
TOTALPROMEDIO = int(os.environ["TOTALPROMEDIO"])
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALCUENTAPROM = int(os.environ["TOTALCUENTAPROM"])

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'


class Transformador:
    def __init__(self):
        self.stopWords = set(stopwords.words('english')) | set(stopwords.words('french'))
        self.colaTransformador = MessageMiddlewareQueue(MOMHOST, COLATRANSFORMADOR + "_" + str(ID))
        self.colaSumTop = [MessageMiddlewareQueue(MOMHOST, COLASUMTOP + "_" + str(i)) for i in range(TOTALSUMTOP)]
        self.colaCuentaProm = [MessageMiddlewareQueue(MOMHOST, COLACUENTAPROM + "_" + str(i)) for i in range(TOTALCUENTAPROM)]
        self.colaPromedio = [MessageMiddlewareQueue(MOMHOST, COLAPROMEDIO + "_" + str(i)) for i in range(TOTALPROMEDIO)]

        self.contador = contadorEof(TOTALCLASIFICADORES)


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
        # Se suma el clienteId para que la misma secuencia de distintos clientes no caiga siempre en el mismo nodo
        particion = mensajeLote.clienteId.int + secuencia
        self.colaCuentaProm[particion % TOTALCUENTAPROM].send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, cuentaPromedio, secuencia).aBytes())
        self.colaPromedio[nodo].send(CantidadPalabrasLoteMensajeSistema(mensajeLote.clienteId, promedio, secuencia).aBytes())
        self.colaSumTop[particion % TOTALSUMTOP].send(PalabrasLoteMensajeSistema(mensajeLote.clienteId, palabrasSumTop, secuencia).aBytes())


    def _finalizarCliente(self, fin: FinMensajeSistema) -> None:
        clienteId = fin.clienteId
        logging.info(f"Mando EOF de {clienteId} con total {fin.totalMsg}")
        eof = FinMensajeSistema(clienteId, fin.totalMsg, ID).aBytes()

        # Cada nodo de la etapa siguiente espera el EOF de todos los transformadores
        self.colaPromedio[clienteId.int % TOTALPROMEDIO].send(eof)
        for cola in self.colaSumTop + self.colaCuentaProm:
            cola.send(eof)
        self.contador.finalizar(clienteId)


    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
                    self._finalizarCliente(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
                logging.debug(f"Descarto lote {mensaje.secuencia} de {mensaje.clienteId}: cliente ya finalizado")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                self.colaCuentaProm.send(bytes)
                self.colaSumTop.send(bytes)
                for i in range(TOTALPROMEDIO):
                    self.colaPromedio[i].send(bytes)
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.info(e)
            logging.info(traceback.format_exc())
            nack()


    def iniciar(self):
        latido = Latido(self.colaTransformador.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        thread_contador = threading.Thread(target=self.contador.iniciar, daemon=True)
        thread_contador.start()
        self.colaTransformador.start_consuming(self.procesarMensaje)
        self._close_connections()


    def _close_connections(self):
        self.colaTransformador.close()
        for cola in self.colaSumTop:
            cola.close()
        for cola in self.colaCuentaProm:
            cola.close()
        for cola in self.colaPromedio:
            cola.close()


    def manejarSigterm(self) -> None:
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
