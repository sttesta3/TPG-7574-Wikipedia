import os
import signal
import logging
import traceback
import threading
from latido import Latido
from contadorEof import contadorEof
from wal import Wal, LineaLog, Recipient
from middleware import MessageMiddlewareQueue
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema, ETAPA_AGREGADOR, origenGateway, ClienteMuertoMensajeSistema
import json 

MOMHOST = os.environ["MOMHOST"]
COLASUMTOP = os.environ["COLASUMTOP"]
COLARESPUESTAS = os.environ["COLARESPUESTAS"]
COLATOPPARCIAL = os.environ["COLATOPPARCIAL"]
COLATOPGLOBAL = os.environ["COLATOPGLOBAL"]
TOTALSUMTOP = int(os.environ["TOTALSUMTOP"])
TOTALTOPGLOBAL = int(os.environ["TOTALTOPGLOBAL"])
TOP_SIZE=20
LOTE = 100
ID = os.environ["ID"]

class PalabrasPorIdioma:
    def __init__(self, bytes=None):
        self.palabras: dict[str, list] = json.loads(bytes.decode("utf-8")) if bytes else {}

    def add(self, cantidad: int, lenguaje, palabra: str) -> bool:
        '''
        recibe lenguaje, palabra, cantidad 
        actualiza la lista de palabras y devuelve True para la PRIMERA detección de palabra compartida  
        '''
        duplicada = False
        actual = self.palabras.get(palabra, [0,{}]) # [conteo de apariciones de la palabra, { idioma: 1 } (tabla de hash de idiomas)]
        actual[0] += cantidad
        if not lenguaje in actual[1]:
            actual[1][lenguaje] = 1
            # Nota: Esta pensado para dos idiomas 
            duplicada = len(actual[1]) == 2
        self.palabras[palabra] = actual
        return duplicada

    def mergeTop(self) -> dict[str, int]:
        result = {}
        for clave, valor in self.palabras.items():
            result[clave] = valor[0]
        return result

    def serialize(self) -> dict[str, list]:
        return self.palabras
            

class AgregadorTop:
    def __init__(self):
        self.colaTopParcial = MessageMiddlewareQueue(MOMHOST, COLATOPPARCIAL + "_" + str(ID))
        self.colaTopGlobal = [MessageMiddlewareQueue(MOMHOST, COLATOPGLOBAL + "_" + str(i)) for i in range(TOTALTOPGLOBAL)]
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
         
        self.clientes = {}
        self.contador = contadorEof(TOTALSUMTOP)
        self.wal = Wal()

    def _procesarData(self, mensajes: PalabrasLoteMensajeSistema) -> None:
        mensaje = mensajes.mensajes[0]
        clienteId = mensajes.clienteId
        if clienteId not in self.clientes:
            self.clientes[clienteId] = PalabrasPorIdioma()

        duplicadas = []
        tanda = 0
        for clave, valor in mensaje.palabras.items():
            if self.clientes[clienteId].add(palabra=clave, cantidad=valor, lenguaje=mensaje.lenguaje):
                # Palabra duplicada.
                duplicadas.append(clave)
                if len(duplicadas) == LOTE:
                    idRespuesta = (ETAPA_AGREGADOR, int(ID), mensajes.secuencia, tanda)
                    mensaje_salida = Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes()
                    self.colaRespuestas.send(mensaje_salida)
                    duplicadas = []
                    tanda += 1
        if len(duplicadas) > 0:
            idRespuesta = (ETAPA_AGREGADOR, int(ID), mensajes.secuencia, tanda)
            mensaje_salida = Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes()
            self.colaRespuestas.send(mensaje_salida)


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            palabras = self.clientes.pop(mensaje.clienteId, PalabrasPorIdioma())
            mensaje_eof = FinMensajeSistema(mensaje.clienteId, origen=origenGateway(ETAPA_AGREGADOR, int(ID))).aBytes()
            self.colaRespuestas.send(mensaje_eof)

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            mensaje_top_global = PalabrasLoteMensajeSistema(mensaje.clienteId, [PalabrasMensajeSistema( palabras=self._top20(palabras.mergeTop()), url="", lenguaje=0)], int(ID)).aBytes()
            self.colaTopGlobal[nodo].send(mensaje_top_global)
            
            mensaje_eof = FinMensajeSistema(mensaje.clienteId, origen=int(ID)).aBytes()
            self.colaTopGlobal[nodo].send(mensaje_eof)

            self.contador.finalizar(mensaje.clienteId)

    def procesarMensaje(self, bytes, ack, nack):
        try:
            
            mensaje = recvMensajeSistema(bytes)
            self.wal.guardarMensaje(bytes)

            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId) or self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto parcial {mensaje.secuencia} de {mensaje.clienteId}")
            elif isinstance(mensaje, ClienteMuertoMensajeSistema):
                for i in range(TOTALTOPGLOBAL):
                    self.colaTopGlobal[i].send(bytes)
                    self.colaTopParcial.send(bytes)
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            
            if self.wal.tiempoDeCheckpoint():
                self.wal.guardarEstado(self.clientes, self.contador.state())
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()


    def _recuperarse(self):
        try:
            self.clientes, contador = self.wal.recuperarEstado()
            self.contador.load_state(contador)

            for logBytes in self.wal.recuperarMensajes():
                log = recvMensajeSistema(logBytes)

                if isinstance(log, FinMensajeSistema):
                    if self.contador.eofRecibido(log.clienteId, log.origen):
                        self._finalizarCliente(log.clienteId)
                        self.contador.finalizar(log.clienteId)
                elif self.contador.yaFinalizado(log.clienteId) or self.contador.yaProcesado(log.clienteId, log.secuencia):
                    logging.debug(f"Descarto lote {log.secuencia} de {log.clienteId}")
                else:
                    self.contador.procesado(log.clienteId, log.secuencia)
                    self._procesarData(log)
        except Exception as e:
            print(f"{e}")
            print(traceback.format_exc())


    def iniciar(self):
        
        self._recuperarse()
        
        latido = Latido(self.colaTopParcial.connection)
        thread_latido = threading.Thread(target=latido.start, daemon=True)
        thread_latido.start()

        self.colaTopParcial.start_consuming(self.procesarMensaje)
        self._close_connections()


    def manejarSigterm(self) -> None:
        self.colaTopParcial.remote_stop()


    def _close_connections(self):
        self.colaTopParcial.close()
        for cola in self.colaTopGlobal:
            cola.close()


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    agregadorTop = AgregadorTop()
    signal.signal(signal.SIGTERM, lambda signum, frame: agregadorTop.manejarSigterm())
    agregadorTop.iniciar()
    return 0


if __name__ == "__main__":
    main()
