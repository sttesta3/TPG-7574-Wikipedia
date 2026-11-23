import os
import sys
import logging
import signal
import traceback
from middleware import MessageMiddlewareQueue
from contadorEof import contadorEof
from protocolo.mensajesSistema import recvMensajeSistema, FinMensajeSistema, PalabrasLoteMensajeSistema, PalabrasMensajeSistema, Respuesta3MensajeSistema, ETAPA_AGREGADOR, origenGateway


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
    def __init__(self):
        self.palabras = {}

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
    
class AgregadorTop:
    def __init__(self):
        self.colaTopParcial = MessageMiddlewareQueue(MOMHOST, COLATOPPARCIAL + "_" + str(ID))
        self.colaTopGlobal = [MessageMiddlewareQueue(MOMHOST, COLATOPGLOBAL + "_" + str(i)) for i in range(TOTALTOPGLOBAL)]
        self.colaRespuestas = MessageMiddlewareQueue(MOMHOST, COLARESPUESTAS)
         
        self.clientes = {}
        self.contador = contadorEof(TOTALSUMTOP)


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
                    self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes())
                    duplicadas = []
                    tanda += 1
        if len(duplicadas) > 0:
            idRespuesta = (ETAPA_AGREGADOR, int(ID), mensajes.secuencia, tanda)
            self.colaRespuestas.send(Respuesta3MensajeSistema(clienteId, duplicadas, idRespuesta).aBytes())


    def _top20(self, palabras: dict[str, int]) -> dict[str, int]:
        top = sorted(palabras.items(), key=lambda item: item[1], reverse=True)
        return dict(top[:TOP_SIZE])

    def _procesarEOF(self, mensaje: FinMensajeSistema) -> None:
        if self.contador.eofRecibido(mensaje.clienteId, mensaje.origen):
            palabras = self.clientes.pop(mensaje.clienteId, PalabrasPorIdioma())
            self.colaRespuestas.send(FinMensajeSistema(mensaje.clienteId, origen=origenGateway(ETAPA_AGREGADOR, int(ID))).aBytes())

            nodo = mensaje.clienteId.int % TOTALTOPGLOBAL
            self.colaTopGlobal[nodo].send(PalabrasLoteMensajeSistema(mensaje.clienteId, [PalabrasMensajeSistema( palabras=self._top20(palabras.mergeTop()), url="", lenguaje=0)], int(ID)).aBytes())
            self.colaTopGlobal[nodo].send(FinMensajeSistema(mensaje.clienteId, origen=int(ID)).aBytes())

            self.contador.finalizar(mensaje.clienteId)
            

    def procesarMensaje(self, bytes, ack, nack):
        try:
            mensaje = recvMensajeSistema(bytes)
            if isinstance(mensaje, FinMensajeSistema):
                self._procesarEOF(mensaje)
            elif self.contador.yaFinalizado(mensaje.clienteId):
                logging.info(f"Descarto parcial de {mensaje.clienteId}: cliente ya finalizado")
            elif self.contador.yaProcesado(mensaje.clienteId, mensaje.secuencia):
                logging.info(f"Descarto parcial {mensaje.secuencia} de {mensaje.clienteId}: duplicado")
            else:
                self._procesarData(mensaje)
                self.contador.procesado(mensaje.clienteId, mensaje.secuencia)
            ack()
        except Exception as e:
            logging.warning(e)
            logging.warning(traceback.format_exc())
            nack()

    def iniciar(self):
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
